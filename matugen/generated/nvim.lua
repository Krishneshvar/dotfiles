-- Matugen generated highlights for Neovim
local colors = {
  bg = "#121318",
  fg = "#e3e1e9",
  primary = "#b5c4ff",
  on_primary = "#1c2d61",
  secondary = "#c1c5dd",
  tertiary = "#e2bbdb",
  error = "#ffb4ab",
  surface = "#292a2f",
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
