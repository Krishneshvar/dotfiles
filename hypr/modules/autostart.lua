---- AUTOSTART ----
-- See https://wiki.hypr.land/Configuring/Basics/Autostart/
-- Autostart necessary processes (like notifications daemons, status bars, etc.)

local terminal          = "kitty"

hl.on("hyprland.start", function () 
hl.exec_cmd(terminal)
hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP HYPRLAND_INSTANCE_SIGNATURE")
hl.exec_cmd("systemctl --user start hyprpolkitagent")
-- hl.exec_cmd("qs -c noctalia-shell")
hl.exec_cmd("awww-daemon")
hl.exec_cmd("~/.config/wallengine/themectl random")
hl.exec_cmd("hypridle")
hl.exec_cmd("hyprlock")
hl.exec_cmd("wl-paste --type text --watch cliphist store")
hl.exec_cmd("wl-paste --type image --watch cliphist store")
hl.exec_cmd("swaync")
hl.exec_cmd("swayosd-server")
hl.exec_cmd("waybar")
end)
