#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

cache_dir = os.path.expanduser("~/.cache/cliphist/thumbs")
os.makedirs(cache_dir, exist_ok=True)

rofi_theme = os.path.expanduser("~/.config/rofi/clipboard.rasi")
clear_tag = "🗑️  Clear All Clipboard History"

def get_menu_entries():
    try:
        res = subprocess.run(["cliphist", "list"], capture_output=True, text=True, check=True)
        lines = res.stdout.splitlines()
    except Exception:
        return []

    entries = []
    # Always put the clear action at the top
    entries.append(f"{clear_tag}\0icon\x1fuser-trash")

    # Process items
    for line in lines:
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        item_id = parts[0]
        content = parts[1] if len(parts) > 1 else ""

        if content.startswith("[[ binary data"):
            thumb_path = os.path.join(cache_dir, f"{item_id}.png")
            if not os.path.exists(thumb_path):
                try:
                    dec = subprocess.Popen(["cliphist", "decode"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    dec_out, _ = dec.communicate(input=f"{item_id}\t".encode())
                    ff = subprocess.Popen(
                        ["ffmpeg", "-i", "-", "-vf", "scale=120:120:force_original_aspect_ratio=decrease", thumb_path, "-y", "-loglevel", "quiet"],
                        stdin=subprocess.PIPE
                    )
                    ff.communicate(input=dec_out)
                except Exception:
                    pass

            details = content.replace("[[ binary data", "").replace("]]", "").strip()
            label = f"{item_id}\t󰋩 Image ({details})"
            if os.path.exists(thumb_path):
                entries.append(f"{label}\0icon\x1f{thumb_path}")
            else:
                entries.append(f"{label}\0icon\x1fimage-x-generic")
        else:
            entries.append(f"{line}\0icon\x1fedit-copy")

    return entries

def main():
    while True:
        entries = get_menu_entries()
        if len(entries) <= 1:
            # Only clear tag or empty
            subprocess.run([
                "rofi", "-dmenu",
                "-theme", rofi_theme,
                "-p", " Clipboard",
                "-mesg", "Clipboard history is empty"
            ], input="Clipboard is empty\n", text=True)
            sys.exit(0)

        menu_data = "\n".join(entries)

        proc = subprocess.Popen([
            "rofi", "-dmenu",
            "-theme", rofi_theme,
            "-p", " Clipboard",
            "-mesg", "<b>Enter</b>: Copy  |  <b>Alt+Del / Right-Click</b>: Delete item",
            "-kb-custom-1", "Alt+Delete,Alt+d",
            "-me-accept-custom", "MouseSecondary",
            "-show-icons"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        selected, _ = proc.communicate(input=menu_data)
        exit_code = proc.returncode

        if exit_code == 1 or not selected:
            # Esc or cancelled
            sys.exit(0)

        selected = selected.strip()

        # Exit code 0: Normal Enter
        if exit_code == 0:
            if selected == clear_tag:
                # Prompt confirmation
                conf = subprocess.run([
                    "rofi", "-dmenu",
                    "-theme", rofi_theme,
                    "-p", "Clear history?",
                    "-mesg", "Are you sure you want to wipe all clipboard history?"
                ], input="✓ Clear all\n✗ Cancel\n", capture_output=True, text=True).stdout.strip()

                if conf == "✓ Clear all":
                    subprocess.run(["cliphist", "wipe"], check=False)
                    shutil.rmtree(cache_dir, ignore_errors=True)
                    os.makedirs(cache_dir, exist_ok=True)
                    subprocess.run(["notify-send", "Clipboard", "History cleared", "-i", "edit-clear"], check=False)
                sys.exit(0)
            else:
                # Extract id before tab
                item_id = selected.split("\t", 1)[0]
                dec = subprocess.Popen(["cliphist", "decode"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                dec_out, _ = dec.communicate(input=f"{item_id}\t".encode())
                wl = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
                wl.communicate(input=dec_out)
                sys.exit(0)

        # Exit code 10: Alt+Delete / Alt+d / Right-Click (Selective delete)
        elif exit_code == 10:
            if selected == clear_tag:
                sys.exit(0)
            else:
                item_id = selected.split("\t", 1)[0]
                dec = subprocess.Popen(["cliphist", "delete"], stdin=subprocess.PIPE)
                dec.communicate(input=f"{item_id}\t".encode())
                thumb = os.path.join(cache_dir, f"{item_id}.png")
                if os.path.exists(thumb):
                    try:
                        os.remove(thumb)
                    except Exception:
                        pass
                # Loop continues to refresh the list in-place!

if __name__ == "__main__":
    main()
