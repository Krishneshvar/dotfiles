return {
  "lukas-reineke/indent-blankline.nvim",
  main = "ibl",
  opts = {
    indent = {
      char = "▎", -- Clean thin line
    },
    scope = {
      show_start = true, -- Highlights the beginning of the current scope
      show_end = false,
      highlight = { "Function", "Label" }, -- Uses existing theme colors for the scope line
    },
    exclude = {
      filetypes = { "help", "alpha", "dashboard", "neo-tree", "Trouble", "lazy" },
    },
  },
}
