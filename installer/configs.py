"""
Configuration symlinking and user environment setup.
"""

import shutil
import stat
from pathlib import Path
from installer.ui import Style, info, success, warn


def backup_and_link(src: Path, dest: Path, dry_run: bool = False) -> bool:
    """Safely symlinks src to dest, backing up existing files/directories if needed."""
    if not src.exists():
        warn(f"Source not found: {src}")
        return False

    if dest.is_symlink():
        try:
            if dest.resolve() == src.resolve():
                print(f"    {Style.GRAY}Already linked:{Style.RESET} {dest.name} -> {src.name}")
                return True
        except Exception:
            pass
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN] Re-link symlink:{Style.RESET} {dest}")
        else:
            dest.unlink()
    elif dest.exists():
        backup = dest.with_name(f"{dest.name}.backup")
        c = 1
        while backup.exists():
            backup = dest.with_name(f"{dest.name}.backup.{c}")
            c += 1
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN] Backup:{Style.RESET} {dest} -> {backup}")
        else:
            print(f"    {Style.YELLOW}Backup:{Style.RESET} {dest} -> {backup.name}")
            shutil.move(dest, backup)

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"    {Style.DIM}[DRY-RUN] Link:{Style.RESET} {src} -> {dest}")
    else:
        dest.symlink_to(src)
        success(f"Linked {Style.BOLD}{dest.name}{Style.RESET}")

    return True


def setup_user_configs(dotfiles_dir: Path, dry_run: bool = False):
    """Sets up ~/.config directories, portals, starship, zsh, media directories, and permissions."""
    config_dir = Path.home() / ".config"
    config_dir.mkdir(parents=True, exist_ok=True)

    folders = [
        "hypr",
        "kitty",
        "matugen",
        "rofi",
        "swaync",
        "swayosd",
        "wallengine",
        "waybar",
        "wlogout",
    ]

    info("Linking configuration directories to ~/.config/ ...")
    for f in folders:
        src = dotfiles_dir / f
        dest = config_dir / f
        backup_and_link(src, dest, dry_run=dry_run)

    # Portal configuration for xdg-desktop-portal
    portal_conf = dotfiles_dir / "hypr" / "hyprland-portals.conf"
    if portal_conf.is_file():
        dest_portal = config_dir / "xdg-desktop-portal" / "hyprland-portals.conf"
        backup_and_link(portal_conf, dest_portal, dry_run=dry_run)

    # Starship prompt configuration
    starship_src = dotfiles_dir / "starship.toml"
    starship_dest = config_dir / "starship.toml"
    if starship_src.is_file() and not starship_dest.exists():
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN] Copy default starship.toml{Style.RESET}")
        else:
            shutil.copy2(starship_src, starship_dest)
            success("Installed starship.toml")

    # Shell configuration (.zshrc)
    zshrc_src = dotfiles_dir / ".zshrc"
    if zshrc_src.is_file():
        backup_and_link(zshrc_src, Path.home() / ".zshrc", dry_run=dry_run)

    # Media Directories & Default Wallpapers
    info("Ensuring media directories exist...")
    wallpapers_dest = Path.home() / "Pictures" / "Wallpapers"
    screenshots_dest = Path.home() / "Pictures" / "Screenshots"
    if not dry_run:
        wallpapers_dest.mkdir(parents=True, exist_ok=True)
        screenshots_dest.mkdir(parents=True, exist_ok=True)
    success("Pictures/Wallpapers and Pictures/Screenshots directories ready.")

    wallpapers_src = dotfiles_dir / "wallengine" / "Wallpapers"
    if wallpapers_src.is_dir():
        info("Installing default wallpapers and themes into ~/Pictures/Wallpapers/ ...")
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN] Copy default wallpapers from {wallpapers_src} to {wallpapers_dest}{Style.RESET}")
        else:
            try:
                shutil.copytree(wallpapers_src, wallpapers_dest, dirs_exist_ok=True)
                success("Default wallpapers and themes populated.")
            except Exception as e:
                warn(f"Failed to copy wallpapers: {e}")

    # Permissions on executable scripts
    info("Setting executable permissions on helper scripts...")
    script_dirs = [dotfiles_dir / "hypr" / "scripts", dotfiles_dir / "wallengine"]
    for d in script_dirs:
        if not d.is_dir():
            continue
        for script in d.iterdir():
            if script.suffix in [".sh", ".py"] or script.name == "themectl":
                if dry_run:
                    print(f"    {Style.DIM}[DRY-RUN] chmod +x {script.name}{Style.RESET}")
                else:
                    try:
                        mode = script.stat().st_mode
                        script.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    except Exception as e:
                        warn(f"Could not chmod {script.name}: {e}")
    success("Permissions configured.")
