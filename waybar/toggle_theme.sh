#!/bin/bash

THEME_DIR="$HOME/.config/waybar/themes"
CURRENT_THEME_LINK="$HOME/.config/waybar/theme.css"
MOCHA="$THEME_DIR/mocha.css"
LATTE="$THEME_DIR/latte.css"

# Initialize if the link doesn't exist
if [ ! -L "$CURRENT_THEME_LINK" ]; then
    ln -sf "$MOCHA" "$CURRENT_THEME_LINK"
    pkill -USR2 waybar
    exit 0
fi

# Toggle logic
if readlink "$CURRENT_THEME_LINK" | grep -q "mocha"; then
    ln -sf "$LATTE" "$CURRENT_THEME_LINK"
    notify-send "Waybar" "Theme switched to Catppuccin Latte" -i "color-management"
else
    ln -sf "$MOCHA" "$CURRENT_THEME_LINK"
    notify-send "Waybar" "Theme switched to Catppuccin Mocha" -i "color-management"
fi

# Reload Waybar styling
pkill -USR2 waybar

