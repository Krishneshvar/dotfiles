"""
Main entry point and orchestrator for the dotfiles installer.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from installer.configs import setup_user_configs
from installer.packages import (
    CONFIG_AUR,
    CONFIG_PACMAN,
    EXTRA_AUR,
    EXTRA_PACMAN,
    install_packages,
    show_package_breakdown,
)
from installer.system import setup_system_wide
from installer.ui import (
    Style,
    box_print,
    error,
    info,
    prompt_input,
    section,
    success,
    warn,
)


def check_network(timeout: int = 3) -> bool:
    """Checks whether an active internet connection is available."""
    import socket
    for host in ["1.1.1.1", "8.8.8.8"]:
        try:
            socket.create_connection((host, 53), timeout=timeout)
            return True
        except OSError:
            pass
    try:
        import urllib.request
        urllib.request.urlopen("https://archlinux.org", timeout=timeout)
        return True
    except Exception:
        return False



def check_git_updates(dotfiles_dir: Path, dry_run: bool = False):
    """Pulls latest commits from remote repository if inside a git work tree."""
    try:
        res = subprocess.run(
            ["git", "-C", str(dotfiles_dir), "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if res.returncode == 0:
            info("Checking for remote repository updates via git...")
            if dry_run:
                print(f"    {Style.DIM}[DRY-RUN] git pull --ff-only{Style.RESET}")
                return
            pull = subprocess.run(
                ["git", "-C", str(dotfiles_dir), "pull", "--ff-only"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if pull.returncode == 0:
                success("Repository is up to date.")
            else:
                warn("Git pull failed or local modifications exist. Continuing with local files.")
    except Exception as e:
        warn(f"Could not check git updates: {e}")


def prompt_package_selection() -> tuple[list[str], list[str]]:
    """Interactive package selection menu."""
    section("Step 1/3", "Package Installation Options")
    print(f"  {Style.BOLD}How would you like to handle package installation?{Style.RESET}\n")
    print(f"    {Style.BOLD}[1]{Style.RESET} {Style.GREEN}Minimal (Config Only){Style.RESET}   Install ONLY packages needed for this desktop setup")
    print(f"                              {Style.GRAY}(51 official + 2 AUR packages){Style.RESET}")
    print(f"    {Style.BOLD}[2]{Style.RESET} {Style.BLUE}Complete (Config + All){Style.RESET} Install config packages + all your personal tools & apps")
    print(f"                              {Style.GRAY}(100 official + 10 AUR packages: dev, nvidia, apps){Style.RESET}")
    print(f"    {Style.BOLD}[3]{Style.RESET} {Style.PEACH}Personal Extras Only{Style.RESET}     Install ONLY your personal apps/tools (skip config pkgs)")
    print(f"                              {Style.GRAY}(49 official + 8 AUR packages){Style.RESET}")
    print(f"    {Style.BOLD}[4]{Style.RESET} {Style.WHITE}Skip Packages{Style.RESET}            Skip package install (proceed straight to dotfiles)")
    print(f"    {Style.BOLD}[v]{Style.RESET} {Style.CYAN}View Package Lists{Style.RESET}       Display full package lists by category")
    print()

    while True:
        choice = prompt_input("Enter choice [1-4 / v] (default: 1): ", default="1")
        if choice == "1":
            return CONFIG_PACMAN, CONFIG_AUR
        elif choice == "2":
            return CONFIG_PACMAN + EXTRA_PACMAN, CONFIG_AUR + EXTRA_AUR
        elif choice == "3":
            return EXTRA_PACMAN, EXTRA_AUR
        elif choice == "4":
            return [], []
        elif choice.lower() == "v":
            show_package_breakdown()
        else:
            print(f"    {Style.RED}Invalid selection. Please choose 1, 2, 3, 4, or v.{Style.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Install and configure dotfiles & system.")
    parser.add_argument("--minimal", action="store_true", help="Install config-required packages only (51 Pacman, 2 AUR)")
    parser.add_argument("--full", action="store_true", help="Install config packages + all personal apps/tools")
    parser.add_argument("--extras-only", action="store_true", help="Install personal apps/tools only")
    parser.add_argument("--skip-packages", action="store_true", help="Skip package installation entirely")
    parser.add_argument("--config-only", action="store_true", help="Only link user configuration files")
    parser.add_argument("--system-only", action="store_true", help="Only run system-wide setup (root required)")
    parser.add_argument("--all", action="store_true", help="Run full installation without interactive prompts")
    parser.add_argument("--no-pull", action="store_true", help="Skip checking git repository updates")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without writing to disk")
    args = parser.parse_args()

    dotfiles_dir = Path(__file__).resolve().parent.parent

    box_print("Hyprland Dotfiles Setup & Installer", "Material You • Waybar • ReGreet • Matugen")

    if args.dry_run:
        print(f"  {Style.YELLOW}⚠ Running in DRY-RUN mode. No changes will be applied to disk.{Style.RESET}\n")

    # Step 0: Check network connectivity
    if not args.config_only and not args.dry_run:
        info("Checking network connectivity...")
        if not check_network():
            error("No internet connection detected.")
            print(f"  {Style.GRAY}An active internet connection is required to install packages and setup components.{Style.RESET}")
            print(f"  {Style.GRAY}Please connect to the internet and rerun the installer.{Style.RESET}\n")
            sys.exit(1)
        success("Network connection is active.")

    # Step 1: Check git updates
    if not args.no_pull and not args.system_only:
        check_git_updates(dotfiles_dir, dry_run=args.dry_run)

    # Step 1: Package Installation
    if not args.config_only and not args.system_only:
        pacman_pkgs: list[str] = []
        aur_pkgs: list[str] = []

        if args.skip_packages:
            info("Skipping package installation (--skip-packages flag).")
        elif args.minimal:
            pacman_pkgs, aur_pkgs = CONFIG_PACMAN, CONFIG_AUR
        elif args.full or args.all:
            pacman_pkgs, aur_pkgs = CONFIG_PACMAN + EXTRA_PACMAN, CONFIG_AUR + EXTRA_AUR
        elif args.extras_only:
            pacman_pkgs, aur_pkgs = EXTRA_PACMAN, EXTRA_AUR
        else:
            pacman_pkgs, aur_pkgs = prompt_package_selection()

        if pacman_pkgs or aur_pkgs:
            install_packages(pacman_pkgs, aur_pkgs, dry_run=args.dry_run)

    # Step 2: User Configurations Setup
    if not args.system_only:
        section("Step 2/3", "User Configuration Files & Symlinks")
        setup_user_configs(dotfiles_dir, dry_run=args.dry_run)

    # Step 3: System-Wide Display Setup
    if not args.config_only:
        run_system = False
        if args.all or args.system_only:
            run_system = True
        else:
            section("Step 3/3", "System-Wide Setup Prompt")
            ans = prompt_input("Do you want to setup system-wide configurations (greetd, PAM, ReGreet)? [y/N]: ", default="n")
            run_system = ans.lower() in ["y", "yes"]

        if run_system:
            setup_system_wide(dotfiles_dir, dry_run=args.dry_run)
        else:
            info("Skipping system-wide configurations.")

    # Finish Banner
    box_print("Installation Complete!", "Restart terminal or reload Hyprland to enjoy your rice")


if __name__ == "__main__":
    main()
