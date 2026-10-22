#!/bin/sh
player_status=$(playerctl status 2>/dev/null)

if [ "$player_status" = "Playing" ] || [ "$player_status" = "Paused" ]; then
    title=$(playerctl metadata --format '{{title}}' 2>/dev/null)
    artist=$(playerctl metadata --format '{{artist}}' 2>/dev/null)
    
    if [ "$player_status" = "Playing" ]; then
        icon="󰎈 "
    else
        icon="󰏥 "
    fi
    
    if [ -n "$title" ]; then
        if [ -n "$artist" ]; then
            text="$title — $artist"
        else
            text="$title"
        fi
        
        # truncate if overly long
        if [ ${#text} -gt 45 ]; then
            text="$(echo "$text" | cut -c 1-42)..."
        fi
        
        echo "$icon $text"
        exit 0
    fi
fi

echo ""
