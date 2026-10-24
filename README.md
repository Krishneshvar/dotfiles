# Dotfiles

A modular Hyprland desktop environment on Arch Linux featuring dynamic Material You theming, automated installer scripts, and a customized ReGreet login experience.

---

## Table of Contents

- [Overview](#overview)
- [Components](#components)
- [Repository Structure](#repository-structure)
- [Wallpapers and Dynamic Theming](#wallpapers-and-dynamic-theming)
- [Installation](#installation)
  - [Automated Installation](#automated-installation)
  - [Installer Command-Line Options](#installer-command-line-options)
  - [Manual Installation](#manual-installation)
- [System-Wide Setup](#system-wide-setup)
- [Keybinds Reference](#keybinds-reference)

---

## Overview

This repository contains personal configuration files and automation scripts for an Arch Linux setup running Hyprland. Colors across the entire desktop (Waybar, Rofi, Kitty, SwayNC, SwayOSD, and wlogout) dynamically adapt to the active wallpaper using Matugen.

---

## Components

| Component | Software | Description |
| :--- | :--- | :--- |
| Window Manager | Hyprland | Dynamic tiling Wayland compositor |
| Bar | Waybar | Modular status bar with workspaces, media, audio, network, and battery |
| Application Launcher | Rofi (Wayland) | App launcher, emoji picker (rofimoji), and keybinds list |
| Clipboard Manager | Cliphist + Rofi | Clipboard history with inline image preview support |
| Notifications | SwayNC | Notification center and control panel |
| OSD | SwayOSD | On-screen indicators for volume, brightness, and caps lock |
| Terminal | Kitty | GPU-accelerated terminal emulator |
| Shell | Zsh + Starship | Zsh with autosuggestions, syntax highlighting, and Starship prompt |
| Wallpaper Daemon | awww | Wayland wallpaper daemon with animated transitions |
| Color Generation | Matugen | Material You palette generator applied across all UI components |
| Power Menu | wlogout | Custom logout interface with dynamic color-matched vector icons |
| Display Manager | greetd + ReGreet | Wayland greeter with GTK4 styling, enlarged clock, and session handling |
| Screen Capture | Hyprshot + Hyprpicker | Screen capture utility and Wayland color picker |

---

## Repository Structure

```text
dotfiles/
├── .zshrc               # Zsh shell configuration
├── starship.toml        # Starship cross-shell prompt configuration
├── install.sh           # Bootstrap shell script (prerequisite checker)
├── install.py           # Installer entry point
├── installer/           # Modular Python installer package
│   ├── configs.py       # User symlink management and backup logic
│   ├── main.py          # Installer orchestration and CLI argument parsing
│   ├── packages.py      # Categorized package lists and package manager runner
│   ├── system.py        # System-level setup (greetd, PAM, wayland-sessions)
│   └── ui.py            # Terminal formatting and output helpers
├── hypr/                # Hyprland configuration, idle, lock, and helper scripts
├── kitty/               # Kitty terminal styling and configurations
├── matugen/             # Color scheme templates for dynamic theming
├── rofi/                # App launcher, clipboard, and keybinds menus
├── setup-files/         # System files for greetd, ReGreet, PAM, and sessions
├── swaync/              # SwayNotificationCenter configuration and styling
├── swayosd/             # SwayOSD styling
├── wallengine/          # Wallpaper/theme switcher (themectl) and bundled Wallpapers/
├── waybar/              # Waybar layout, modules, and styles
└── wlogout/             # Power menu layout, styles, and vector icons
```

---

## Wallpapers and Dynamic Theming

Wallpapers and themes are managed by the `themectl` utility located in `wallengine/themectl`. Default themes and wallpapers are bundled inside `wallengine/Wallpapers/` and automatically copied to `~/Pictures/Wallpapers/` by the installer so theming works out of the box.

The repository includes pre-generated color schemes in `matugen/generated/` and matching vector icons in `wlogout/icons/` based on the default `Catppuccin` theme (`Space.png`). This ensures that Waybar, Rofi, SwayNC, Kitty, and Hyprlock load styled immediately on first boot without experiencing cold-start race conditions. When a user subsequently selects another wallpaper or theme, `themectl` generates and applies updated palettes dynamically.


### Organization

Wallpapers are stored in your home directory under `~/Pictures/Wallpapers/`:

```text
~/Pictures/Wallpapers/
├── Abstract/
│   ├── Reflected Orange Building.jpg
│   └── Tile Windowed Building.jpg
├── Catppuccin/
│   ├── Artificial Valley.jpg
│   ├── Basement.jpg
│   ├── Bluehour.jpg
│   └── Space.png
├── Scenery/
│   └── Valley Train.jpg
└── Tokyo Night/
    └── Cafe At Night.png
```

- Each subdirectory inside `~/Pictures/Wallpapers/` represents a theme name.
- Image files inside each theme directory represent wallpapers for that theme.

### How Dynamic Theming Works

When a wallpaper is selected using `themectl`:
1. `awww` applies the image with a smooth transition.
2. `matugen` extracts the color palette from the image and generates `colors.css`.
3. `themectl` triggers live reload signals for Waybar, SwayNC, Kitty, and SwayOSD.
4. `wlogout` SVG icons are updated to match the active foreground and accent colors.
5. Hyprland configuration is reloaded.

---

## Installation

### Automated Installation

The provided installer automates package installation, user configuration symlinking with conflict backups, and system-wide greeter configuration.

1. Clone the repository:
   ```bash
   git clone https://github.com/Krishneshvar/dotfiles.git
   cd dotfiles
   ```

2. Run the bootstrap installer:
   ```bash
   ./install.sh
   ```

The script will:
- Verify that `git` and `python` are installed on the system (installing them via `pacman` if missing).
- Launch the Python installer wizard.
- Prompt you to select your desired package installation scope:
  - **Minimal (Config Only)**: Installs only the 49 official packages and 2 AUR packages strictly needed for the desktop environment.
  - **Complete (Config + All)**: Installs config packages plus personal development tools, compilers, NVIDIA drivers, and applications.
  - **Personal Extras Only**: Installs only the personal extras (dev tools, compilers, drivers, productivity apps).
  - **Skip Packages**: Skips package installation and proceeds directly to linking configurations.
  - **View Package Lists**: Displays a categorized breakdown of all packages.
- Symlink all configuration directories to `~/.config/`, creating `.backup` copies of existing files.
- Prompt to configure system-wide files (ReGreet, greetd, PAM) requiring `sudo`.

You can also run the Python installer directly:
```bash
python3 install.py
```

### Installer Command-Line Options

The installer supports non-interactive execution and targeted workflows:

```text
usage: install.py [-h] [--minimal] [--full] [--extras-only] [--skip-packages]
                  [--config-only] [--system-only] [--all] [--no-pull]
                  [--dry-run]

Options:
  -h, --help       Show this help message and exit
  --minimal        Install config-required packages only (49 Pacman, 2 AUR)
  --full           Install config packages and personal applications
  --extras-only    Install personal applications and tools only
  --skip-packages  Skip package installation entirely
  --config-only    Only link user configuration files
  --system-only    Only run system-wide setup (root required)
  --all            Run full installation without interactive prompts
  --no-pull        Skip checking git repository updates
  --dry-run        Simulate actions without writing to disk
```

Examples:
```bash
# Preview what will be changed without modifying the system
./install.sh --dry-run

# Link user configuration files only, skipping package installation
python3 install.py --config-only --skip-packages

# Perform a minimal install without interactive prompts
./install.sh --minimal --all
```

---

### Manual Installation

If you prefer to link configurations manually:

1. Clone the repository to a directory of your choice (for example, `~/dotfiles`).

2. Link configuration directories into `~/.config/`:
   ```bash
   mkdir -p ~/.config
   ln -snf ~/dotfiles/hypr ~/.config/hypr
   ln -snf ~/dotfiles/kitty ~/.config/kitty
   ln -snf ~/dotfiles/matugen ~/.config/matugen
   ln -snf ~/dotfiles/rofi ~/.config/rofi
   ln -snf ~/dotfiles/swaync ~/.config/swaync
   ln -snf ~/dotfiles/swayosd ~/.config/swayosd
   ln -snf ~/dotfiles/wallengine ~/.config/wallengine
   ln -snf ~/dotfiles/waybar ~/.config/waybar
   ln -snf ~/dotfiles/wlogout ~/.config/wlogout
   ```

3. Link individual configuration files:
   ```bash
   # Portal configuration
   mkdir -p ~/.config/xdg-desktop-portal
   ln -snf ~/dotfiles/hypr/hyprland-portals.conf ~/.config/xdg-desktop-portal/hyprland-portals.conf

   # Starship prompt
   cp ~/dotfiles/starship.toml ~/.config/starship.toml

   # Zsh configuration
   ln -snf ~/dotfiles/.zshrc ~/.zshrc
   ```

4. Create required directories, copy bundled wallpapers, and set script permissions:
   ```bash
   mkdir -p ~/Pictures/Wallpapers ~/Pictures/Screenshots
   cp -rn ~/dotfiles/wallengine/Wallpapers/* ~/Pictures/Wallpapers/
   chmod +x ~/dotfiles/hypr/scripts/*.sh ~/dotfiles/hypr/scripts/*.py ~/dotfiles/wallengine/themectl
   ```

---

## System-Wide Setup

The login screen uses `greetd` paired with `ReGreet` running under a minimal Hyprland Wayland session.

To apply system-wide configurations manually:

```bash
# Wayland session desktop entry
sudo mkdir -p /usr/share/wayland-sessions
sudo cp -v setup-files/hyprland.desktop /usr/share/wayland-sessions/

# PAM configurations
sudo mkdir -p /etc/pam.d
sudo cp -v setup-files/login /etc/pam.d/login
sudo cp -v setup-files/greetd /etc/pam.d/greetd

# Greetd and ReGreet configuration
sudo mkdir -p /etc/greetd
sudo cp -v setup-files/config.toml /etc/greetd/config.toml
sudo cp -v setup-files/hyprland.lua /etc/greetd/hyprland.lua
sudo cp -v setup-files/regreet.toml /etc/greetd/regreet.toml
sudo cp -v setup-files/regreet.css /etc/greetd/regreet.css
sudo cp -v setup-files/wallpaper.png /etc/greetd/wallpaper.png
sudo chmod 644 /etc/greetd/*

# Greeter permissions and log directory
sudo usermod -aG video greeter
sudo mkdir -p /var/log/regreet
sudo chown -R greeter:greeter /var/log/regreet

# Enable display manager service
sudo systemctl enable greetd.service
```

---

## Keybinds Reference

A quick reference list of default keybindings configured in `hypr/modules/keybinds.lua`:

| Keybinding | Action |
| :--- | :--- |
| `Super + Space` | Open Rofi application launcher |
| `Super + Q` | Open Kitty terminal |
| `Super + E` | Open Nautilus file manager |
| `Super + C` | Close active window |
| `Super + T` | Toggle floating window mode |
| `Super + F11` | Toggle fullscreen mode |
| `Super + V` | Clipboard history (Cliphist) |
| `Super + /` | Show keybindings list (Rofi) |
| `Super + .` | Open emoji picker (Rofimoji) |
| `Super + N` | Toggle notification center (SwayNC) |
| `Super + Shift + N` | Toggle Do Not Disturb (SwayNC) |
| `Super + L` | Lock screen (Hyprlock) |
| `Super + Escape` | Open wlogout power menu |
| `Super + M` | Exit Hyprland session |
| `Super + Shift + W` | Select wallpaper (themectl) |
| `Super + Shift + T` | Select theme (themectl) |
| `Super + Shift + R` | Apply random theme and wallpaper (themectl) |
| `Super + Shift + S` | Capture region screenshot (Hyprshot) |
| `Print` | Capture active window screenshot (Hyprshot) |
| `Super + Left / Right / Up / Down` | Move window focus |
| `Super + Shift + , / .` | Swap columns (Scrolling layout) |
| `Super + 1 .. 0` | Switch to workspace 1 through 10 |
| `Super + Shift + 1 .. 0` | Move active window to workspace 1 through 10 |
| `Super + Mouse Scroll` | Cycle through workspaces |
| `Super + LMB / RMB (drag)` | Move or resize floating window |
| `Volume / Brightness / Media Keys` | Audio, brightness, and media playback control |

