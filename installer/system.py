"""
System-wide setup: display manager (greetd / ReGreet), PAM, and Wayland session entries.
"""

import subprocess
from pathlib import Path
from installer.ui import Style, alert, error, info, success, warn


def detect_conflicting_display_managers() -> list[str]:
    """Detect any active or enabled display managers other than greetd."""
    conflicting = set()

    # 1. Check /etc/systemd/system/display-manager.service symlink
    dm_symlink = Path("/etc/systemd/system/display-manager.service")
    if dm_symlink.is_symlink():
        try:
            target = dm_symlink.resolve().name
            if target.endswith(".service") and target != "greetd.service":
                conflicting.add(target.replace(".service", ""))
        except Exception:
            pass

    # 2. Check well-known display manager services
    known_dms = ["gdm", "sddm", "lightdm", "ly", "lxdm", "lemurs", "nodm", "xdm"]
    for dm in known_dms:
        try:
            res_enabled = subprocess.run(
                ["systemctl", "is-enabled", f"{dm}.service"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            if res_enabled.returncode == 0 and res_enabled.stdout.strip() == "enabled":
                conflicting.add(dm)
                continue

            res_active = subprocess.run(
                ["systemctl", "is-active", f"{dm}.service"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            if res_active.returncode == 0 and res_active.stdout.strip() == "active":
                conflicting.add(dm)
        except Exception:
            pass

    return sorted(list(conflicting))


def setup_system_wide(dotfiles_dir: Path, dry_run: bool = False):
    """Copies greetd configs, ReGreet theme, PAM login, and wayland sessions to system paths."""
    setup_dir = dotfiles_dir / "setup-files"
    if not setup_dir.is_dir():
        error(f"setup-files directory not found in {dotfiles_dir}")
        return

    def run_cmd(cmd: list[str]):
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN]{Style.RESET} {' '.join(cmd)}")
            return
        subprocess.run(cmd, check=True)

    # Detect and handle conflicting display managers
    conflicting_dms = detect_conflicting_display_managers()
    if conflicting_dms:
        dm_names = ", ".join(f"{dm}.service" for dm in conflicting_dms)
        alert(
            "Conflicting Display Manager Detected",
            f"The following display manager is currently configured:\n"
            f"  • {dm_names}\n\n"
            f"Running multiple display managers causes login crashes and session conflicts.\n"
            f"We are stopping and disabling {dm_names} and will install and run greetd instead."
        )
        for dm in conflicting_dms:
            info(f"Disabling and stopping {dm}.service...")
            try:
                run_cmd(["sudo", "systemctl", "disable", f"{dm}.service"])
                run_cmd(["sudo", "systemctl", "stop", f"{dm}.service"])
            except Exception as e:
                warn(f"Failed to stop/disable {dm}.service: {e}")

    copies = [
        (setup_dir / "hyprland.desktop", Path("/usr/share/wayland-sessions/hyprland.desktop"), "644"),
        (setup_dir / "login", Path("/etc/pam.d/login"), "644"),
        (setup_dir / "greetd", Path("/etc/pam.d/greetd"), "644"),
        (setup_dir / "config.toml", Path("/etc/greetd/config.toml"), "644"),
        (setup_dir / "hyprland.lua", Path("/etc/greetd/hyprland.lua"), "644"),
        (setup_dir / "regreet.toml", Path("/etc/greetd/regreet.toml"), "644"),
        (setup_dir / "regreet.css", Path("/etc/greetd/regreet.css"), "644"),
        (setup_dir / "wallpaper.png", Path("/etc/greetd/wallpaper.png"), "644"),
    ]

    info("Installing system configurations (requires sudo)...")
    for src, dest, perm in copies:
        if not src.is_file():
            warn(f"Missing {src.name}. Skipping.")
            continue
        print(f"    {Style.CYAN}→{Style.RESET} {src.name} -> {dest}")
        run_cmd(["sudo", "mkdir", "-p", str(dest.parent)])
        run_cmd(["sudo", "cp", "-v", str(src), str(dest)])
        run_cmd(["sudo", "chmod", perm, str(dest)])

    # Configure greeter user permissions & log directory
    try:
        chk = subprocess.run(["id", "greeter"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if chk.returncode == 0:
            info("Configuring greeter user permissions and cache directory...")
            run_cmd(["sudo", "usermod", "-aG", "video", "greeter"])
            run_cmd(["sudo", "mkdir", "-p", "/var/log/regreet"])
            run_cmd(["sudo", "chown", "-R", "greeter:greeter", "/var/log/regreet"])
    except Exception:
        pass

    # Enable greetd display manager service
    try:
        srv = subprocess.run(
            ["systemctl", "list-unit-files", "greetd.service"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if "greetd.service" in srv.stdout:
            info("Enabling greetd.service...")
            run_cmd(["sudo", "systemctl", "enable", "--force", "greetd.service"])
    except Exception:
        pass

    success("System-wide display manager and session setup complete.")
