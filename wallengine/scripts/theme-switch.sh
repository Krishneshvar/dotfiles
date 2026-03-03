#!/bin/bash

THEMES_DIR="$HOME/.config/themes"
STATE_DIR="$HOME/.config/wallengine/state"

THEME="$1"

if [ ! -d "$THEMES_DIR/$THEME" ]; then
    echo "Theme does not exist"
    exit 1
fi

WALL=$(find "$THEMES_DIR/$THEME" -type f | shuf -n 1)

echo "$THEME" > "$STATE_DIR/current_theme"
echo "$WALL" > "$STATE_DIR/current_wallpaper"

swww img "$WALL" \
  --transition-type grow \
  --transition-duration 1 \
  --transition-fps 30

matugen image "$WALL"

hyprctl reload
pkill -SIGUSR2 waybar 2>/dev/null
