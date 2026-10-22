#!/bin/sh
out=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ 2>/dev/null)

[ -z "$out" ] && exit 0

if echo "$out" | grep -q "MUTED"; then
    echo "󰝟 Muted"
else
    vol=$(echo "$out" | awk '{print int($2 * 100)}')
    if [ "$vol" -ge 60 ]; then
        icon=""
    elif [ "$vol" -ge 25 ]; then
        icon=""
    else
        icon=""
    fi
    echo "$icon ${vol}%"
fi
