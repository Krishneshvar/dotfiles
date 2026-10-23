"""
System-wide setup: display manager (greetd / ReGreet), PAM, and Wayland session entries.
"""

import subprocess
from pathlib import Path
from installer.ui import Style, error, info, success, warn


def setup_system_wide(dotfiles_dir: Path, dry_run: bool = False):
    """Copies greetd configs, ReGreet theme, PAM login, and wayland sessions to system paths."""
    setup_dir = dotfiles_dir / "setup-files"
    if not setup_dir.is_dir():
        error(f"setup-files directory not found in {dotfiles_dir}")
        return

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

    def run_cmd(cmd: list[str]):
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN]{Style.RESET} {' '.join(cmd)}")
            return
        subprocess.run(cmd, check=True)

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
            run_cmd(["sudo", "systemctl", "enable", "greetd.service"])
    except Exception:
        pass

    success("System-wide display manager and session setup complete.")
