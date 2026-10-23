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
    # Fonts
    "ttf-jetbrains-mono-nerd",
    "noto-fonts",
    "noto-fonts-emoji",
    "noto-fonts-cjk",
    "noto-fonts-extra",
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


def install_packages(pacman_pkgs: list[str], aur_pkgs: list[str], dry_run: bool = False):
    """Installs official packages via pacman/AUR helper and AUR packages via yay/paru."""
    if not pacman_pkgs and not aur_pkgs:
        info("No packages to install.")
        return

    helper = detect_aur_helper()

    def run_cmd(cmd: list[str]):
        if dry_run:
            print(f"    {Style.DIM}[DRY-RUN]{Style.RESET} {' '.join(cmd)}")
            return
        subprocess.run(cmd, check=True)

    if helper:
        info(f"Using AUR helper: {Style.BOLD}{helper}{Style.RESET}")
        if pacman_pkgs:
            info(f"Installing {len(pacman_pkgs)} official packages...")
            run_cmd([helper, "-S", "--needed"] + pacman_pkgs)
        if aur_pkgs:
            info(f"Installing {len(aur_pkgs)} AUR packages...")
            run_cmd([helper, "-S", "--needed"] + aur_pkgs)
    else:
        info(f"No AUR helper found. Using {Style.BOLD}pacman{Style.RESET} for official packages...")
        if pacman_pkgs:
            run_cmd(["sudo", "pacman", "-S", "--needed"] + pacman_pkgs)
        if aur_pkgs:
            warn("The following AUR packages must be installed manually (or install yay/paru first):")
            print(f"    {Style.PEACH}{' '.join(aur_pkgs)}{Style.RESET}")

    success("Package installation step completed.")
