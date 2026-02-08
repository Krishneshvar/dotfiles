-- Matugen generated highlights for Neovim
local colors = {
  bg = "{{ colors.background.default.hex }}",
  fg = "{{ colors.on_background.default.hex }}",
  primary = "{{ colors.primary.default.hex }}",
  on_primary = "{{ colors.on_primary.default.hex }}",
  secondary = "{{ colors.secondary.default.hex }}",
  tertiary = "{{ colors.tertiary.default.hex }}",
  error = "{{ colors.error.default.hex }}",
  surface = "{{ colors.surface_container_high.default.hex }}",
}

-- UI Base
vim.api.nvim_set_hl(0, "Normal", { bg = colors.bg, fg = colors.fg })
vim.api.nvim_set_hl(0, "NormalFloat", { bg = colors.surface, fg = colors.fg })
vim.api.nvim_set_hl(0, "FloatBorder", { bg = colors.surface, fg = colors.primary })
vim.api.nvim_set_hl(0, "CursorLine", { bg = colors.surface })

-- Telescope Modern Look
vim.api.nvim_set_hl(0, "TelescopeBorder", { fg = colors.primary })
vim.api.nvim_set_hl(0, "TelescopePromptPrefix", { fg = colors.tertiary })

-- Diagnostics (Modern & Clear)
vim.api.nvim_set_hl(0, "DiagnosticError", { fg = colors.error })
vim.api.nvim_set_hl(0, "DiagnosticWarn", { fg = colors.tertiary })
vim.api.nvim_set_hl(0, "DiagnosticInfo", { fg = colors.secondary })
vim.api.nvim_set_hl(0, "DiagnosticHint", { fg = colors.primary })

-- Visual Selection
vim.api.nvim_set_hl(0, "Visual", { bg = colors.primary, fg = colors.on_primary })
