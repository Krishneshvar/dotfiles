#!/usr/bin/env bash

# If rofi wifi menu is already running, toggle it off
if pgrep -f "rofi_wifi.py" > /dev/null; then
    pkill -f "rofi_wifi.py"
    pkill -x "rofi"
    exit 0
fi

python3 "$HOME/.config/waybar/scripts/rofi_wifi.py" &
