-- /etc/greetd/hyprland.lua
-- Minimal greeter compositor configuration for ReGreet

hl.on("hyprland.start", function()
    hl.exec_cmd("regreet; hyprctl dispatch exit")
end)

hl.monitor({
    output   = "",
    mode     = "preferred",
    position = "auto",
    scale    = "1",
})

hl.config({
    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        disable_autoreload       = true,
    },
    animations = {
        enabled = false,
    },
})
