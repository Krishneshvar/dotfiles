---- KEYBINDINGS ----

local mainMod = "SUPER"

local p = require("modules.programs")
local terminal     = p.terminal
local fileManager  = p.fileManager
local menu         = p.menu
local swaync       = p.swaync
local cliphist     = p.cliphist
local rofimoji     = p.rofimoji
local wall_script  = p.wall_script
local theme_script = p.theme_script
local rand_theme   = p.rand_theme
local hyprshot_w   = p.hyprshot_w
local hyprshot_r   = p.hyprshot_r
local wlogout      = p.wlogout

-- Example binds, see https://wiki.hypr.land/Configuring/Basics/Binds/ for more
hl.bind(mainMod .. " + Q", hl.dsp.exec_cmd(terminal))
local closeWindowBind = hl.bind(mainMod .. " + C", hl.dsp.window.close())
-- closeWindowBind:set_enabled(false)
hl.bind(mainMod .. " + M", hl.dsp.exec_cmd(wlogout))
hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + space", hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + J", hl.dsp.layout("togglesplit"))    -- dwindle only
hl.bind(mainMod .. " + T", hl.dsp.window.float({ action = "toggle" }))

-- Session & Power Management
hl.bind(mainMod .. " + ESCAPE", hl.dsp.exec_cmd(wlogout))
hl.bind(mainMod .. " + L", hl.dsp.exec_cmd("hyprlock"))

-- Notifications & Control Center
hl.bind(mainMod .. " + N", hl.dsp.exec_cmd(swaync))
hl.bind(mainMod .. " + SHIFT + N", hl.dsp.exec_cmd("swaync-client -d -t")) -- toggle Do Not Disturb

-- Custom binds
hl.bind(mainMod .. " + V", hl.dsp.exec_cmd(cliphist))
hl.bind(mainMod .. " + period", hl.dsp.exec_cmd(rofimoji))
hl.bind(mainMod .. " + SHIFT + W", hl.dsp.exec_cmd(wall_script))
hl.bind(mainMod .. " + SHIFT + T", hl.dsp.exec_cmd(theme_script))
hl.bind(mainMod .. " + SHIFT + R", hl.dsp.exec_cmd(rand_theme))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.exec_cmd(hyprshot_r))
hl.bind("PRINT", hl.dsp.exec_cmd(hyprshot_w))

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
-- Swap columns
hl.bind(mainMod .. " + SHIFT + period", hl.dsp.exec_cmd("layoutmsg, swapcol r"))
hl.bind(mainMod .. " + SHIFT + comma",  hl.dsp.exec_cmd("layoutmsg, swapcol l"))

-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("swayosd-client --output-volume raise"),      { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("swayosd-client --output-volume lower"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("swayosd-client --output-volume mute-toggle"), { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("swayosd-client --input-volume mute-toggle"),  { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("swayosd-client --brightness raise"),         { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("swayosd-client --brightness lower"),         { locked = true, repeating = true })

-- Requires playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),       { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),   { locked = true })
