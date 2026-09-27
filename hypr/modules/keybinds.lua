---- KEYBINDINGS ----

local mainMod = "SUPER"

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


-- Example binds, see https://wiki.hypr.land/Configuring/Basics/Binds/ for more
hl.bind(mainMod .. " + Q", hl.dsp.exec_cmd(terminal))
local closeWindowBind = hl.bind(mainMod .. " + C", hl.dsp.window.close())
-- closeWindowBind:set_enabled(false)
hl.bind(mainMod .. " + M", hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"))
hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + T", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + A", hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + J", hl.dsp.layout("togglesplit"))    -- dwindle only

-- Custom binds
hl.bind(mainMod .. " + N", hl.dsp.exec_cmd(swaync))
hl.bind(mainMod .. " + V", hl.dsp.exec_cmd(cliphist))
-- hl.bind(mainMod .. " + period", hl.dsp.exec_cmd(rofimoji))
hl.bind(mainMod .. " + W", hl.dsp.exec_cmd(wall_script))
hl.bind(mainMod .. " + T", hl.dsp.exec_cmd(theme_script))
hl.bind(mainMod .. " + R", hl.dsp.exec_cmd(rand_theme))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.exec_cmd(hyprshot_r))
hl.bind("PRINT", hl.dsp.exec_cmd(hyprshot_w))

-- Noctalia binds
hl.bind(mainMod .. " + SPACE", hl.dsp.exec_cmd(noctalia_launcher))
hl.bind(mainMod .. " + S", hl.dsp.exec_cmd(noctalia_controlcenter))

-- Move focus with mainMod + arrow keys
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down" }))

-- Switch workspaces with mainMod + [0-9]
-- Move active window to a workspace with mainMod + SHIFT + [0-9]
for i = 1, 10 do
    local key = i % 10 -- 10 maps to key 0
    hl.bind(mainMod .. " + " .. key,         hl.dsp.focus({ workspace = i}))
    hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end

-- Scroll through existing workspaces with mainMod + scroll
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))

-- Move/resize windows with mainMod + LMB/RMB and dragging
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Hyprland Scrolling layout binds
-- Move focus between columns
-- hl.bind(mainMod .. " + period", hl.dsp.exec_cmd())
-- hl.bind(mainMod .. " + comma", hl.dsp.exec_cmd())
-- bind = $mainMod, period, layoutmsg, move +col
-- bind = $mainMod, comma, layoutmsg, move -col
-- # Swap columns
-- bind = $mainMod SHIFT, period, layoutmsg, swapcol r
-- bind = $mainMod SHIFT, comma, layoutmsg, swapcol l

-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+ && swayosd-client --volume raise"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%- && swayosd-client --volume lower"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle && swayosd-client --volume mute"),      { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle && swayosd-client --mic mute"),       { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+ && swayosd-client --brightness raise"),              { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%- && swayosd-client --brightness lower"),              { locked = true, repeating = true })

-- Noctalia laptop multimedia keys
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("qs -c noctalia-shell ipc call volume increase"),     { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("qs -c noctalia-shell ipc call volume decrease"),     { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("qs -c noctalia-shell ipc call volume muteOutput"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("qs -c noctalia-shell ipc call brightness increase"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("qs -c noctalia-shell ipc call brightness decrease"), { locked = true, repeating = true })

-- Requires playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),       { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),   { locked = true })
