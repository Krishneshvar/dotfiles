#!/bin/bash

THEMES_DIR="$HOME/.config/themes"

THEME=$(find "$THEMES_DIR" -mindepth 1 -maxdepth 1 -type d | xargs -n1 basename | rofi -dmenu)

[ -z "$THEME" ] && exit 0

~/.config/wallengine/scripts/theme-switch.sh "$THEME"
