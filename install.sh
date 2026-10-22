#!/usr/bin/env bash

set -e

# Path to the directory where this script resides
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config"

echo "================================"
echo "    Dotfiles Install Script     "
echo "================================"
echo ""

# ---------------------------------------------------------------------------
# 0. Git Pull (Check and update to latest version of configs)
# ---------------------------------------------------------------------------
echo "--> Checking for latest dotfiles updates via git..."
if git -C "$DOTFILES_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Pulling latest changes from remote repository..."
    if git -C "$DOTFILES_DIR" pull --ff-only; then
        echo "✓ Repository is up to date."
    else
        echo "⚠ Warning: Git pull failed or local modifications exist. Continuing with local files."
    fi
else
    echo "Notice: $DOTFILES_DIR is not a git repository. Skipping git pull."
fi
echo ""

# ---------------------------------------------------------------------------
# 1. Package Installation (Check and install dependencies)
# ---------------------------------------------------------------------------
echo "--> Dependencies & Packages"
read -p "Do you want to check and install required packages? [y/N]: " install_pkgs

if [[ "$install_pkgs" =~ ^[Yy]$ ]]; then
    # Detect package manager / AUR helper
    AUR_HELPER=""
    if command -v yay >/dev/null 2>&1; then
        AUR_HELPER="yay"
    elif command -v paru >/dev/null 2>&1; then
        AUR_HELPER="paru"
    fi

    OFFICIAL_PKGS=(
        base-devel
        gcc
        cmake
        cpio
        git
        python
        hyprland
        hyprlock
        hypridle
        hyprpolkitagent
        hyprpicker
        hyprshot
        greetd
        greetd-regreet
        gnome-keyring
        libsecret
        pipewire
        wireplumber
        xdg-desktop-portal
        xdg-desktop-portal-hyprland
        xdg-desktop-portal-gtk
        grim
        slurp
        waybar
        rofi
        kitty
        nautilus
        starship
        matugen
        awww
        swaync
        swayosd
        rofimoji
        zsh
        zsh-completions
        zsh-autosuggestions
        zsh-syntax-highlighting
        cliphist
        wl-clipboard
        wtype
        ffmpeg
        playerctl
        brightnessctl
        pavucontrol
        blueman
        networkmanager
        ttf-jetbrains-mono-nerd
        noto-fonts
        noto-fonts-emoji
        noto-fonts-cjk
        noto-fonts-extra
        python-gobject
        gtk-layer-shell
        python-cairo
        qt6-base
        qt6-svg
        qt6-wayland
        layer-shell-qt
        opencv
        xorg-xwayland
        fastfetch
        power-profiles-daemon
    )

    AUR_PKGS=(
        wlogout
        xwaylandvideobridge
    )

    if [ -n "$AUR_HELPER" ]; then
        echo "Using AUR helper: $AUR_HELPER"
        echo "Installing official packages..."
        $AUR_HELPER -S --needed "${OFFICIAL_PKGS[@]}"
        echo "Installing AUR packages..."
        $AUR_HELPER -S --needed "${AUR_PKGS[@]}"
    else
        echo "No AUR helper (yay/paru) detected. Installing official packages with pacman..."
        sudo pacman -S --needed "${OFFICIAL_PKGS[@]}"
        echo ""
        echo "⚠ Note: The following AUR packages could not be installed automatically:"
        echo "  ${AUR_PKGS[*]}"
        echo "Please install an AUR helper like yay or install them manually."
    fi
fi
echo ""

# ---------------------------------------------------------------------------
# 2. Setup user configuration files (Symlinking ~/.config)
# ---------------------------------------------------------------------------
echo "--> Setting up user configuration files..."
mkdir -p "$CONFIG_DIR"

backup_and_link() {
    local src="$1"
    local dest="$2"

    if [ -e "$dest" ] || [ -h "$dest" ]; then
        if [ -h "$dest" ]; then
            if [ "$(readlink -f "$dest")" = "$(readlink -f "$src")" ]; then
                echo "Already linked: $dest -> $src"
                return 0
            fi
            echo "Updating symlink at $dest"
            rm "$dest"
        else
            echo "Backing up existing $dest to ${dest}.backup"
            mv "$dest" "${dest}.backup"
        fi
    fi

    echo "Linking $src -> $dest"
    ln -s "$src" "$dest"
}

# Link configuration directories present in dotfiles
config_folders=(hypr kitty matugen rofi swaync swayosd wallengine waybar wlogout)
for folder in "${config_folders[@]}"; do
    if [ -d "$DOTFILES_DIR/$folder" ]; then
        backup_and_link "$DOTFILES_DIR/$folder" "$CONFIG_DIR/$folder"
    else
        echo "Warning: Directory $folder not found in $DOTFILES_DIR. Skipping."
    fi
done

# Ensure portal configuration is in place for xdg-desktop-portal
mkdir -p "$CONFIG_DIR/xdg-desktop-portal"
if [ -f "$DOTFILES_DIR/hypr/hyprland-portals.conf" ]; then
    backup_and_link "$DOTFILES_DIR/hypr/hyprland-portals.conf" "$CONFIG_DIR/xdg-desktop-portal/hyprland-portals.conf"
fi

# Setup starship.toml
if [ ! -f "$CONFIG_DIR/starship.toml" ]; then
    if [ -f "$DOTFILES_DIR/starship.toml" ]; then
        echo "Copying default starship.toml to $CONFIG_DIR/starship.toml"
        cp "$DOTFILES_DIR/starship.toml" "$CONFIG_DIR/starship.toml"
    fi
fi

# Link .zshrc
if [ -f "$DOTFILES_DIR/.zshrc" ]; then
    backup_and_link "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
else
    echo "Warning: .zshrc not found. Skipping."
fi

# Ensure Pictures directories exist
mkdir -p "$HOME/Pictures/Wallpapers"
mkdir -p "$HOME/Pictures/Screenshots"

# Set executable permissions on scripts
echo "Setting executable permissions on scripts..."
chmod +x "$DOTFILES_DIR"/hypr/scripts/*.sh "$DOTFILES_DIR"/hypr/scripts/*.py "$DOTFILES_DIR"/wallengine/themectl 2>/dev/null || true

echo "✓ User configuration files have been successfully linked."
echo ""

# ---------------------------------------------------------------------------
# 3. System-wide setup (greetd, PAM, hyprland desktop session)
# ---------------------------------------------------------------------------
echo "--> System-wide setup"
echo "This section requires root privileges and sets up greetd, pam, and hyprland sessions."
read -p "Do you want to setup system-wide configurations? [y/N]: " setup_system

if [[ "$setup_system" =~ ^[Yy]$ ]]; then
    echo "Requesting sudo privileges..."

    if [ -d "$DOTFILES_DIR/setup-files" ]; then
        # Hyprland desktop entry
        if [ -f "$DOTFILES_DIR/setup-files/hyprland.desktop" ]; then
            echo "Copying hyprland.desktop to /usr/share/wayland-sessions/"
            sudo mkdir -p /usr/share/wayland-sessions
            sudo cp -v "$DOTFILES_DIR/setup-files/hyprland.desktop" /usr/share/wayland-sessions/hyprland.desktop
        fi

        # PAM login
        if [ -f "$DOTFILES_DIR/setup-files/login" ]; then
            echo "Copying login to /etc/pam.d/"
            sudo mkdir -p /etc/pam.d
            sudo cp -v "$DOTFILES_DIR/setup-files/login" /etc/pam.d/login
        fi

        # Greetd PAM and Config
        if [ -f "$DOTFILES_DIR/setup-files/greetd" ]; then
            echo "Copying greetd PAM to /etc/pam.d/"
            sudo mkdir -p /etc/pam.d
            sudo cp -v "$DOTFILES_DIR/setup-files/greetd" /etc/pam.d/greetd
        fi

        if [ -f "$DOTFILES_DIR/setup-files/config.toml" ]; then
            echo "Copying greetd config.toml to /etc/greetd/"
            sudo mkdir -p /etc/greetd
            sudo cp -v "$DOTFILES_DIR/setup-files/config.toml" /etc/greetd/config.toml
        fi

        if [ -f "$DOTFILES_DIR/setup-files/hyprland.lua" ]; then
            echo "Copying greetd hyprland.lua to /etc/greetd/"
            sudo mkdir -p /etc/greetd
            sudo cp -v "$DOTFILES_DIR/setup-files/hyprland.lua" /etc/greetd/hyprland.lua
        fi

        # ReGreet configuration, styles, and background
        if [ -f "$DOTFILES_DIR/setup-files/regreet.toml" ]; then
            echo "Copying regreet.toml to /etc/greetd/"
            sudo mkdir -p /etc/greetd
            sudo cp -v "$DOTFILES_DIR/setup-files/regreet.toml" /etc/greetd/regreet.toml
        fi

        if [ -f "$DOTFILES_DIR/setup-files/regreet.css" ]; then
            echo "Copying regreet.css to /etc/greetd/"
            sudo mkdir -p /etc/greetd
            sudo cp -v "$DOTFILES_DIR/setup-files/regreet.css" /etc/greetd/regreet.css
        fi

        if [ -f "$DOTFILES_DIR/setup-files/wallpaper.png" ]; then
            echo "Copying greeter wallpaper to /etc/greetd/"
            sudo mkdir -p /etc/greetd
            sudo cp -v "$DOTFILES_DIR/setup-files/wallpaper.png" /etc/greetd/wallpaper.png
            sudo chmod 644 /etc/greetd/wallpaper.png
        fi

        # Configure greeter user permissions and cache directory
        if id greeter >/dev/null 2>&1; then
            echo "Ensuring greeter user belongs to video group..."
            sudo usermod -aG video greeter 2>/dev/null || true
            sudo mkdir -p /var/log/regreet
            sudo chown -R greeter:greeter /var/log/regreet 2>/dev/null || true
        fi

        # Enable greetd display manager service
        if systemctl list-unit-files greetd.service >/dev/null 2>&1; then
            echo "Enabling greetd.service..."
            sudo systemctl enable greetd.service 2>/dev/null || true
        fi

        echo "✓ System-wide setup complete."
    else
        echo "Error: setup-files directory not found in dotfiles repository."
    fi
else
    echo "Skipping system-wide configurations."
fi

echo ""
echo "================================"
echo "    Installation Complete       "
echo "================================"
echo "Enjoy your setup! Restart your terminal or reload Hyprland for changes to take effect."
