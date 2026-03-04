#!/usr/bin/env bash

# File paths
export SCRIPT_DIR="$HOME/.config/waybar/scripts"
export CAL_SCRIPT="$SCRIPT_DIR/calendar_widget.py"

# Toggle logic
if pgrep -f "python3 $CAL_SCRIPT" > /dev/null; then
    pkill -f "python3 $CAL_SCRIPT"
else
    python3 "$CAL_SCRIPT" &
fi
