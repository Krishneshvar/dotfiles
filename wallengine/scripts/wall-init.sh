#!/bin/bash

STATE_DIR="$HOME/.config/wallengine/state"

WALL="$STATE_DIR/current_wallpaper"

if [ -f "$WALL" ]; then
    swww img "$(cat "$WALL")"
else
    ~/.config/wallengine/scripts/wall-random.sh
fi
