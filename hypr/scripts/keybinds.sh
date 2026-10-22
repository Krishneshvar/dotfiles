#!/usr/bin/env bash

# Keybindings rofi launcher script

THEME_FILE="$HOME/.config/rofi/keybinds.rasi"

# Entries format: Display text | Command to execute | Icon name
read -r -d '' ENTRIES << 'EOF'
<b>SUPER + SPACE</b>          <span alpha='65%'>·  Launch Applications</span>|rofi -show drun -theme ~/.config/rofi/launcher.rasi|applications-system
<b>SUPER + Q</b>              <span alpha='65%'>·  Open Terminal (kitty)</span>|kitty|kitty
<b>SUPER + E</b>              <span alpha='65%'>·  Open File Manager (nautilus)</span>|nautilus|system-file-manager
<b>SUPER + V</b>              <span alpha='65%'>·  Clipboard History (cliphist)</span>|~/.config/hypr/scripts/cliphist.sh|edit-copy
<b>SUPER + .</b>              <span alpha='65%'>·  Emoji Picker (rofimoji)</span>|rofimoji --selector rofi --selector-args '-theme ~/.config/rofi/emoji.rasi' --clipboarder wl-copy --typer wtype --hidden-descriptions|face-smile
<b>SUPER + /</b>              <span alpha='65%'>·  Show Keybindings</span>|~/.config/hypr/scripts/keybinds.sh|preferences-desktop-keyboard
<b>SUPER + SHIFT + S</b>      <span alpha='65%'>·  Screenshot Region (hyprshot)</span>|hyprshot -m region --freeze -o ~/Pictures/Screenshots|applets-screenshooter
<b>PRINT</b>                  <span alpha='65%'>·  Screenshot Window (hyprshot)</span>|hyprshot -m window --freeze -o ~/Pictures/Screenshots|applets-screenshooter
<b>SUPER + SHIFT + W</b>      <span alpha='65%'>·  Wallpaper Selector</span>|~/.config/wallengine/themectl choose-wall|preferences-desktop-wallpaper
<b>SUPER + SHIFT + T</b>      <span alpha='65%'>·  Theme Selector</span>|~/.config/wallengine/themectl choose-theme|preferences-desktop-theme
<b>SUPER + SHIFT + R</b>      <span alpha='65%'>·  Random Theme & Wallpaper</span>|~/.config/wallengine/themectl random|media-playlist-shuffle
<b>SUPER + N</b>              <span alpha='65%'>·  Toggle Notification Center</span>|swaync-client --skip-wait -t|preferences-system-notifications
<b>SUPER + SHIFT + N</b>      <span alpha='65%'>·  Toggle Do Not Disturb</span>|swaync-client -d -t|preferences-system-notifications
<b>SUPER + L</b>              <span alpha='65%'>·  Lock Screen (hyprlock)</span>|hyprlock|system-lock-screen
<b>SUPER + ESCAPE</b>         <span alpha='65%'>·  Power / Logout Menu (wlogout)</span>|wlogout|system-shutdown
<b>SUPER + C</b>              <span alpha='65%'>·  Close Active Window</span>|hyprctl dispatch killactive|window-close
<b>SUPER + T</b>              <span alpha='65%'>·  Toggle Floating Window</span>|hyprctl dispatch togglefloating|view-restore
<b>SUPER + P</b>              <span alpha='65%'>·  Toggle Pseudo Tiling</span>|hyprctl dispatch pseudo|view-grid
<b>SUPER + J</b>              <span alpha='65%'>·  Toggle Split Direction</span>|hyprctl dispatch togglesplit|view-grid
<b>SUPER + Arrow Keys</b>     <span alpha='65%'>·  Focus Window (Left / Right / Up / Down)</span>||input-keyboard
<b>SUPER + LMB (drag)</b>     <span alpha='65%'>·  Move Window</span>||input-mouse
<b>SUPER + RMB (drag)</b>     <span alpha='65%'>·  Resize Window</span>||input-mouse
<b>SUPER + [1 - 9, 0]</b>     <span alpha='65%'>·  Switch to Workspace 1 - 10</span>||preferences-desktop-display
<b>SUPER + SHIFT + [0-9]</b>  <span alpha='65%'>·  Move Window to Workspace 1 - 10</span>||preferences-desktop-display
<b>SUPER + Mouse Scroll</b>   <span alpha='65%'>·  Cycle Workspaces</span>||input-mouse
<b>SUPER + SHIFT + , / .</b>  <span alpha='65%'>·  Swap Columns (Scrolling layout)</span>||view-grid
<b>Audio Keys</b>             <span alpha='65%'>·  Raise / Lower / Mute Volume</span>||audio-volume-high
<b>Brightness Keys</b>        <span alpha='65%'>·  Adjust Screen Brightness</span>||video-display
<b>Media Keys</b>             <span alpha='65%'>·  Play / Pause / Next / Prev Track</span>||media-playback-start
EOF

MENU_ITEMS=""
while IFS="|" read -r display cmd icon; do
    [ -z "$display" ] && continue
    MENU_ITEMS="${MENU_ITEMS}${display}\0icon\x1f${icon}\n"
done <<< "$ENTRIES"

SELECTED=$(printf "%b" "$MENU_ITEMS" | rofi -dmenu \
    -theme "$THEME_FILE" \
    -markup-rows \
    -p "⌨ Keybinds" \
    -i)

if [ -n "$SELECTED" ]; then
    CMD=$(echo "$ENTRIES" | grep -F "$SELECTED|" | head -n 1 | cut -d '|' -f 2)
    if [ -n "$CMD" ]; then
        eval "$CMD" &
    fi
fi
