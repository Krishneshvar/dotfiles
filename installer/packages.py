"""
Package definitions and installation management for Arch Linux (pacman, yay, paru).
"""

import shutil
import subprocess
from installer.ui import Style, box_print, info, success, warn

# ---------------------------------------------------------------------------
# Category A: Strictly Required for Dotfiles & Hyprland Desktop
# ---------------------------------------------------------------------------
CONFIG_PACMAN = [
    # Compositor & Desktop Core
    "hyprland",
    "hyprlock",
    "hypridle",
    "hyprpolkitagent",
    "hyprpicker",
    "hyprshot",
    "xorg-xwayland",
    # Portals & Sound Server
    "xdg-desktop-portal",
    "xdg-desktop-portal-hyprland",
    "xdg-desktop-portal-gtk",
    "pipewire",
    "pipewire-pulse",
    "wireplumber",
    # Bar, Launcher, Notifications, OSD
    "waybar",
    "rofi",
    "rofimoji",
    "wtype",
    "swaync",
    "swayosd",
    # Theming & Wallpaper
    "matugen",
    "awww",
    # Fonts & Icons
    "ttf-jetbrains-mono-nerd",
    "noto-fonts",
    "noto-fonts-emoji",
    "noto-fonts-cjk",
    "noto-fonts-extra",
    "papirus-icon-theme",
    # Shell & Terminal
    "kitty",
    "zsh",
    "zsh-completions",
    "zsh-autosuggestions",
    "zsh-syntax-highlighting",
    "starship",
    "nautilus",
    "fastfetch",
    # Keyring, Clipboard & Media Tools
    "gnome-keyring",
    "libsecret",
    "cliphist",
    "wl-clipboard",
    "ffmpeg",
    "grim",
    "slurp",
    "playerctl",
    "brightnessctl",
    "pavucontrol",
    "blueman",
    "networkmanager",
    "network-manager-applet",
    "power-profiles-daemon",
    # Greeter
    "greetd",
    "greetd-regreet",
    # Python runtime
    "python",
]

CONFIG_AUR = [
    "wlogout",
    "xwaylandvideobridge",
]

# ---------------------------------------------------------------------------
# Category B: User's Additional Personal Packages
# ---------------------------------------------------------------------------
EXTRA_PACMAN = [
    # Base Development & Compilers
    "base-devel",
    "gcc",
    "git",
    "make",
    "rustup",
    "nodejs",
    "npm",
    "jdk-openjdk",
    "jdk21-openjdk",
    "jdk25-openjdk",
    # Editors & Productivity
    "vim",
    "neovim",
    "obsidian",
    "discord",
    "bitwarden",
    # NVIDIA Drivers & Hardware Acceleration
    "nvidia-open",
    "nvidia-utils",
    "nvidia-settings",
    "egl-wayland",
    "libva",
    "libva-utils",
    "libva-nvidia-driver",
    "nvidia-prime",
    # Graphics & Diagnostics
    "mesa",
    "mesa-utils",
    "vulkan-intel",
    # Power & Thermals
    "thermald",
    "powertop",
    # Bluetooth & Network Utilities
    "bluez",
    "bluez-utils",
    "openbsd-netcat",
    "nmap",
    # System & Archive Tools
    "curl",
    "wget",
    "unzip",
    "zip",
    "tree",
    "htop",
    "pacman-contrib",
    "os-prober",
    "gparted",
    "gvfs-mtp",
    "android-udev",
    # Theming & Media GUIs
    "nwg-look",
    "qt5ct",
    "qt6ct",
    "vlc",
    "vlc-plugins-all",
    "foot",
]

EXTRA_AUR = [
    "google-chrome",
    "visual-studio-code-bin",
    "brave-bin",
    "antigravity-ide",
    "spotify-launcher",
    "gpu-screen-recorder",
    "gpu-screen-recorder-gtk",
    "localsend-bin",
]


def detect_aur_helper() -> str:
    """Find available AUR helper (yay or paru)."""
    for helper in ["yay", "paru"]:
        if shutil.which(helper):
            return helper
    return ""


def show_package_breakdown():
    """Prints a detailed categorized list of all packages."""
    box_print("Detailed Package Breakdown", "Categorized Overview")

    dev_pkgs = [p for p in EXTRA_PACMAN if p in ["base-devel", "gcc", "git", "make", "rustup", "nodejs", "npm", "openmpi", "jdk-openjdk", "jdk21-openjdk", "jdk25-openjdk"]]
    editor_pkgs = [p for p in EXTRA_PACMAN if p in ["vim", "neovim", "obsidian", "discord", "bitwarden"]]
    gpu_pkgs = [p for p in EXTRA_PACMAN if p in ["nvidia-open", "nvidia-utils", "nvidia-settings", "egl-wayland", "libva", "libva-utils", "libva-nvidia-driver", "nvidia-prime", "mesa", "mesa-utils", "vulkan-intel"]]
    sys_pkgs = [p for p in EXTRA_PACMAN if p in ["thermald", "powertop", "bluez", "bluez-utils", "openbsd-netcat", "nmap", "curl", "wget", "unzip", "zip", "tree", "htop", "pacman-contrib", "os-prober", "gparted", "gvfs-mtp", "android-udev", "nwg-look", "qt5ct", "qt6ct", "vlc", "vlc-plugins-all", "foot"]]

    categories = {
        "Config Core & Desktop": (CONFIG_PACMAN, CONFIG_AUR),
        "Dev Tools & Compilers": (dev_pkgs, []),
        "Editors & Productivity": (editor_pkgs, []),
        "NVIDIA & Graphics Drivers": (gpu_pkgs, []),
        "System, Power & Diagnostics": (sys_pkgs, []),
        "User AUR Applications": ([], EXTRA_AUR),
    }

    for cat_name, (pac, aur) in categories.items():
        print(f"{Style.BOLD}{Style.CYAN}● {cat_name}{Style.RESET}")
        if pac:
            print(f"  {Style.GRAY}Pacman:{Style.RESET} {', '.join(pac)}")
        if aur:
            print(f"  {Style.PEACH}AUR:{Style.RESET}    {', '.join(aur)}")
        print()


def install_package_batch(base_cmd: list[str], pkgs: list[str], dry_run: bool = False) -> list[str]:
    """
    Attempts batch installation. If batch installation fails, falls back to
    installing packages individually so a single failing package does not abort
    the installation of all other packages.
    Returns a list of packages that failed to install.
    """
    if not pkgs:
        return []

    if dry_run:
        print(f"    {Style.DIM}[DRY-RUN]{Style.RESET} {' '.join(base_cmd + pkgs)}")
        return []

    # 1. Try batch installation first (fastest)
    try:
        res = subprocess.run(base_cmd + pkgs)
        if res.returncode == 0:
            return []
    except Exception as e:
        warn(f"Batch execution error: {e}")

    # 2. Batch failed: fall back to installing packages individually
    warn("Batch installation encountered an issue. Installing packages individually...")
    failed = []
    for pkg in pkgs:
        try:
            p_res = subprocess.run(base_cmd + [pkg])
            if p_res.returncode != 0:
                failed.append(pkg)
        except Exception:
            failed.append(pkg)

    return failed


def install_packages(pacman_pkgs: list[str], aur_pkgs: list[str], dry_run: bool = False):
    """Installs official packages via pacman/AUR helper and AUR packages via yay/paru."""
    if not pacman_pkgs and not aur_pkgs:
        info("No packages to install.")
        return

    helper = detect_aur_helper()
    failed_pacman: list[str] = []
    failed_aur: list[str] = []

    if helper:
        info(f"Using AUR helper: {Style.BOLD}{helper}{Style.RESET}")
        base_cmd = [helper, "-S", "--needed", "--noconfirm"]
        if pacman_pkgs:
            info(f"Installing {len(pacman_pkgs)} official packages...")
            failed_pacman = install_package_batch(base_cmd, pacman_pkgs, dry_run=dry_run)
        if aur_pkgs:
            info(f"Installing {len(aur_pkgs)} AUR packages...")
            failed_aur = install_package_batch(base_cmd, aur_pkgs, dry_run=dry_run)
    else:
        info(f"No AUR helper found. Using {Style.BOLD}pacman{Style.RESET} for official packages...")
        if pacman_pkgs:
            failed_pacman = install_package_batch(["sudo", "pacman", "-S", "--needed", "--noconfirm"], pacman_pkgs, dry_run=dry_run)
        if aur_pkgs:
            warn("The following AUR packages must be installed manually (or install yay/paru first):")
            print(f"    {Style.PEACH}{' '.join(aur_pkgs)}{Style.RESET}")

    total_failed = failed_pacman + failed_aur
    if total_failed:
        warn(f"{len(total_failed)} package(s) could not be installed automatically:")
        for pkg in total_failed:
            print(f"    {Style.RED}✗ {pkg}{Style.RESET}")
        print(f"  {Style.GRAY}Continuing with dotfiles and user configurations...{Style.RESET}")
    else:
        success("Package installation step completed successfully.")

