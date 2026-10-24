---- LOOK AND FEEL ----
-- Refer https://wiki.hypr.land/Configuring/Basics/Variables/

local theme_colors = nil
local colors_chunk = loadfile(os.getenv("HOME") .. "/.config/matugen/generated/hyprland.lua")
if colors_chunk then
    theme_colors = colors_chunk()
end

hl.config({
    general = {
        gaps_in  = 1,
        gaps_out = 5,
        border_size = 2,
        -- Set to true to enable resizing windows by clicking and dragging on borders and gaps
        resize_on_border = true,
        -- Please see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Tearing/ before you turn this on
        allow_tearing = false,

        col = {
            active_border   = theme_colors and ("rgb(" .. theme_colors.primary:gsub("#", "") .. ")") or "rgba(33ccffee)",
            inactive_border = theme_colors and ("rgba(" .. theme_colors.outline:gsub("#", "") .. "aa)") or "rgba(595959aa)",
        },

        layout = "scrolling",
    },

    decoration = {
        rounding       = 5,
        rounding_power = 5,

        -- Change transparency of focused and unfocused windows
        active_opacity   = 1.0,
        inactive_opacity = 0.9,

        shadow = {
            enabled      = false
        },

        blur = {
            enabled   = false,
            size      = 3,
            passes    = 2,
            vibrancy  = 0.1696,
        },
    },

    animations = {
        enabled = false
    },

    -- See https://wiki.hypr.land/Configuring/Layouts/Scrolling-Layout/ for more
    scrolling = {
        fullscreen_on_one_column = true,
        column_width             = 0.9,
        direction                = "right", -- New windows appear to the right
        focus_fit_method         = 0,     -- 0 = center, 1 = fit
        follow_focus             = true,
        follow_min_visible       = 0.4,
    },
})
