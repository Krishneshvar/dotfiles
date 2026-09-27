-- Hyprland config wiki for reference
-- https://wiki.hypr.land/Configuring/Start/

---- IMPORTS ----
require("modules.monitors")
require("modules.programs")
require("modules.autostart")
require("modules.env")
require("modules.permissions")
require("modules.lookandfeel")
require("modules.input")
require("modules.keybinds")
require("modules.windowrules")


---- MY PROGRAMS ----
-- Set programs that you use

local terminal          = "kitty"
local fileManager       = "nautilus"
local menu              = "rofi -show drun -theme ~/.config/rofi/launcher.rasi"
local swaync            = "swaync-client --skip-wait -t"
local cliphist          = "cliphist list | rofi -dmenu -theme ~/.config/rofi/clipboard.rasi | cliphist decode | wl-copy"
local rofimoji          = "rofimoji --selector rofi --selector-args '-theme ~/.config/rofi/emoji.rasi' --clipboarder wl-copy --typer wtype --hidden-descriptions"
local wall_script       = "~/.config/wallengine/themectl choose-wall"
local theme_script      = "~/.config/wallengine/themectl choose-theme"
local rand_theme        = "~/.config/wallengine/themectl random"
local hyprshot_w        = "hyprshot -m window --freeze"
local hyprshot_r        = "hyprshot -m region --freeze"
local noctalia_ipc      = "qs -c noctalia-shell ipc call"
local noctalia_launcher = "qs -c noctalia-shell ipc call launcher toggle"
local noctalia_controlcenter = "qs -c noctalia-shell ipc call controlCenter toggle"
