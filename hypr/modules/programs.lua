---- DEFAULT PROGRAMS ----
-- Central source of truth for user applications across Hyprland modules

local programs = {
    terminal     = "kitty",
    fileManager  = "nautilus",
    menu         = "rofi -show drun -theme ~/.config/rofi/launcher.rasi",
    swaync       = "swaync-client --skip-wait -t",
    cliphist     = "~/.config/hypr/scripts/cliphist.sh",
    rofimoji     = "rofimoji --selector rofi --selector-args '-theme ~/.config/rofi/emoji.rasi' --clipboarder wl-copy --typer wtype --hidden-descriptions",
    wall_script  = "~/.config/wallengine/themectl choose-wall",
    theme_script = "~/.config/wallengine/themectl choose-theme",
    rand_theme   = "~/.config/wallengine/themectl random",
    hyprshot_w   = "hyprshot -m window --freeze",
    hyprshot_r   = "hyprshot -m region --freeze",
    wlogout      = "wlogout",
}

return programs
