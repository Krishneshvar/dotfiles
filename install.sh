#!/usr/bin/env bash

set -e

# Path to the directory where this script resides
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config"

echo "================================"
echo "    Dotfiles Install Script     "
echo "================================"
echo ""

# Ensure ~/.config exists
mkdir -p "$CONFIG_DIR"

backup_and_link() {
    local src="$1"
    local dest="$2"

    if [ -e "$dest" ] || [ -h "$dest" ]; then
        if [ ! -h "$dest" ]; then
            echo "Backing up existing $dest to ${dest}.backup"
            mv "$dest" "${dest}.backup"
        else
            echo "Removing existing symlink at $dest"
            rm "$dest"
        fi
    fi

    echo "Linking $src -> $dest"
    ln -s "$src" "$dest"
}

echo "--> Setting up user configuration files..."

# 1. Link folders in ~/.config
config_folders=(hypr kitty matugen nvim rofi scripts swaync swayosd wallengine waybar)
for folder in "${config_folders[@]}"; do
    if [ -d "$DOTFILES_DIR/$folder" ]; then
        backup_and_link "$DOTFILES_DIR/$folder" "$CONFIG_DIR/$folder"
    else
        echo "Warning: Directory $folder not found in $DOTFILES_DIR. Skipping."
    fi
done

# 2. Link starship.toml
if [ -f "$DOTFILES_DIR/starship.toml" ]; then
    backup_and_link "$DOTFILES_DIR/starship.toml" "$CONFIG_DIR/starship.toml"
else
    echo "Warning: starship.toml not found. Skipping."
fi

# 3. Link .zshrc
if [ -f "$DOTFILES_DIR/.zshrc" ]; then
    backup_and_link "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
else
    echo "Warning: .zshrc not found. Skipping."
fi

echo "User configuration files have been successfully linked."
echo ""

# 4. System-wide setup
echo "--> System-wide setup"
echo "This section requires root privileges and sets up greetd, pam, and hyprland sessions."
read -p "Do you want to setup system-wide configurations? [y/N]: " setup_system

if [[ "$setup_system" =~ ^[Yy]$ ]]; then
    echo "Requesting sudo privileges..."
    
    # Check if necessary setup files exist before copying
    if [ -d "$DOTFILES_DIR/setup-files" ]; then
        
        # hyprland desktop entry
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

        if [ -f "$DOTFILES_DIR/setup-files/hyprland.conf" ]; then
            echo "Copying greetd hyprland.conf to /etc/greetd/"
            sudo mkdir -p /etc/greetd
            sudo cp -v "$DOTFILES_DIR/setup-files/hyprland.conf" /etc/greetd/hyprland.conf
        fi

        echo "System-wide setup complete."
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
echo "Enjoy your new setup! You may need to restart your terminal or log out and log back in for changes to take effect."
