#!/usr/bin/env python3
import subprocess
import sys
import os
import re

THEME_PATH = os.path.expanduser("~/.config/rofi/wifi.rasi")

def run_cmd(cmd, check=False):
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=check)
        return res.stdout.strip()
    except Exception:
        return ""

def notify(summary, body="", icon="network-wireless"):
    try:
        subprocess.run(["notify-send", "-a", "Wi-Fi", "-i", icon, summary, body])
    except Exception:
        pass

def rofi_menu(options, prompt="Wi-Fi", mesg=None):
    cmd = ["rofi", "-dmenu", "-i", "-p", prompt]
    if os.path.exists(THEME_PATH):
        cmd.extend(["-theme", THEME_PATH])
    if mesg:
        cmd.extend(["-mesg", mesg])
    
    input_text = "\n".join(options)
    res = subprocess.run(cmd, input=input_text, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        return res.stdout.strip()
    return None

def rofi_password(prompt="Password:"):
    cmd = ["rofi", "-dmenu", "-password", "-p", prompt]
    if os.path.exists(THEME_PATH):
        cmd.extend(["-theme", THEME_PATH])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        return res.stdout.strip()
    return None

def get_wifi_status():
    status = run_cmd(["nmcli", "radio", "wifi"])
    return status.lower() == "enabled"

def get_saved_connections():
    out = run_cmd(["nmcli", "-t", "-f", "TYPE,NAME", "connection", "show"])
    saved = set()
    for line in out.splitlines():
        if line.startswith("802-11-wireless:"):
            saved.add(line.split("802-11-wireless:", 1)[1])
    return saved

def get_wifi_icon(signal, is_secure):
    try:
        sig = int(signal)
    except Exception:
        sig = 0
    if is_secure:
        if sig >= 75: return "󰤪"
        if sig >= 50: return "󰤧"
        if sig >= 25: return "󰤤"
        return "󰤡"
    else:
        if sig >= 75: return "󰤨"
        if sig >= 50: return "󰤥"
        if sig >= 25: return "󰤢"
        return "󰤟"

def main():
    if not get_wifi_status():
        choice = rofi_menu([
            "󰤨   Enable Wi-Fi",
            "   Open Network Settings"
        ], prompt="Wi-Fi: Disabled")
        if choice and "Enable" in choice:
            run_cmd(["nmcli", "radio", "wifi", "on"])
            notify("Wi-Fi Enabled", "Scanning for networks...")
        elif choice and "Settings" in choice:
            subprocess.Popen(["nm-connection-editor"])
        return

    # Fetch available networks
    raw_list = run_cmd(["nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY", "device", "wifi", "list"])
    saved_conns = get_saved_connections()

    networks = {}
    connected_ssid = None

    for line in raw_list.splitlines():
        if not line: continue
        parts = [re.sub(r"\\(.)", r"\1", p) for p in re.split(r"(?<!\\):", line)]
        if len(parts) < 4: continue
        in_use, ssid, signal, security = parts[0], parts[1], parts[2], parts[3]
        if not ssid: continue
        
        try:
            sig_val = int(signal)
        except Exception:
            sig_val = 0
            
        is_in_use = (in_use.strip() == "*")
        if is_in_use:
            connected_ssid = ssid
            
        is_secure = bool(security and security.strip() and security.strip() != "--")
        
        if ssid not in networks or sig_val > networks[ssid]["signal"]:
            networks[ssid] = {
                "in_use": is_in_use,
                "signal": sig_val,
                "secure": is_secure,
                "security_str": security
            }

    # Build menu items
    menu_items = []
    ssid_map = {}

    # Header actions
    menu_items.append("󰤮   Disable Wi-Fi")
    menu_items.append("󰑐   Rescan Networks")
    menu_items.append("󰤨   Connect to Hidden Network")

    # If connected, show connected network at top
    if connected_ssid and connected_ssid in networks:
        data = networks[connected_ssid]
        icon = get_wifi_icon(data["signal"], data["secure"])
        item = f"{icon}   {connected_ssid}  (Connected  {data['signal']}%)"
        menu_items.append(item)
        ssid_map[item] = connected_ssid

    # List remaining networks sorted by signal
    sorted_ssids = sorted(
        [s for s in networks if s != connected_ssid],
        key=lambda s: networks[s]["signal"],
        reverse=True
    )

    for ssid in sorted_ssids:
        data = networks[ssid]
        icon = get_wifi_icon(data["signal"], data["secure"])
        saved_mark = "  [Saved]" if ssid in saved_conns else ""
        item = f"{icon}   {ssid}  ({data['signal']}%){saved_mark}"
        menu_items.append(item)
        ssid_map[item] = ssid

    choice = rofi_menu(menu_items, prompt="Wi-Fi")
    if not choice:
        return

    if choice == "󰤮   Disable Wi-Fi":
        run_cmd(["nmcli", "radio", "wifi", "off"])
        notify("Wi-Fi Disabled")
        return

    if choice == "󰑐   Rescan Networks":
        notify("Scanning...", "Looking for Wi-Fi networks...")
        run_cmd(["nmcli", "device", "wifi", "rescan"])
        main()
        return

    if choice == "󰤨   Connect to Hidden Network":
        hidden_ssid = rofi_menu([], prompt="Enter SSID:")
        if not hidden_ssid: return
        pwd = rofi_password(prompt=f"Password for {hidden_ssid}:")
        if pwd is None: return
        notify("Connecting...", f"Connecting to {hidden_ssid}...")
        cmd = ["nmcli", "device", "wifi", "connect", hidden_ssid]
        if pwd:
            cmd.extend(["password", pwd])
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            notify("Connected", f"Successfully connected to {hidden_ssid}")
        else:
            notify("Connection Failed", res.stderr.strip() or "Unknown error", icon="network-error")
        return

    selected_ssid = ssid_map.get(choice)
    if not selected_ssid:
        return

    # If selected network is already connected
    if selected_ssid == connected_ssid:
        action = rofi_menu([
            f"󰖪   Disconnect from {selected_ssid}",
            f"   Forget {selected_ssid}",
            "󰅖   Cancel"
        ], prompt=selected_ssid)
        if action and "Disconnect" in action:
            run_cmd(["nmcli", "connection", "down", "id", selected_ssid])
            notify("Disconnected", f"Disconnected from {selected_ssid}")
        elif action and "Forget" in action:
            run_cmd(["nmcli", "connection", "delete", "id", selected_ssid])
            notify("Network Forgotten", f"Deleted saved profile for {selected_ssid}")
        return

    # If network is already saved in NetworkManager, try connection up
    if selected_ssid in saved_conns:
        notify("Connecting...", f"Connecting to {selected_ssid}...")
        res = subprocess.run(["nmcli", "connection", "up", "id", selected_ssid],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            notify("Connected", f"Connected to {selected_ssid}")
            return

    data = networks[selected_ssid]
    if data["secure"]:
        pwd = rofi_password(prompt=f"Password for {selected_ssid}:")
        if pwd is None:
            return
        notify("Connecting...", f"Connecting to {selected_ssid}...")
        res = subprocess.run(["nmcli", "device", "wifi", "connect", selected_ssid, "password", pwd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            notify("Connected", f"Connected to {selected_ssid}")
        else:
            notify("Connection Failed", res.stderr.strip() or "Incorrect password", icon="network-error")
    else:
        notify("Connecting...", f"Connecting to {selected_ssid}...")
        res = subprocess.run(["nmcli", "device", "wifi", "connect", selected_ssid],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            notify("Connected", f"Connected to {selected_ssid}")
        else:
            notify("Connection Failed", res.stderr.strip() or "Could not connect", icon="network-error")

if __name__ == "__main__":
    main()
