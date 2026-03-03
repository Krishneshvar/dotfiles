#!/bin/bash

THEMES_DIR="$HOME/.config/themes"
STATE_DIR="$HOME/.config/wallengine/state"

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Pick random theme
THEME=$(find "$THEMES_DIR" -mindepth 1 -maxdepth 1 -type d | shuf -n 1 | xargs basename)

# Pick random wallpaper from that theme
WALL=$(find "$THEMES_DIR/$THEME" -type f | shuf -n 1)

if [ -z "$WALL" ]; then
    echo "No wallpapers found."
    exit 1
fi

# Save state
echo "$THEME" > "$STATE_DIR/current_theme"
echo "$WALL" > "$STATE_DIR/current_wallpaper"

# Set wallpaper
swww img "$WALL" \
  --transition-type grow \
  --transition-duration 1 \
  --transition-fps 30

# Generate theme
matugen image "$WALL"

# Reload UI
hyprctl reload
pkill -SIGUSR2 waybar 2>/dev/null
