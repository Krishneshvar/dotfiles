return {
  "folke/which-key.nvim",
  event = "VeryLazy",
  dependencies = {
    "echasnovski/mini.icons",
    "nvim-tree/nvim-web-devicons"
  },
  opts = {
    win = {
      border = "rounded",
      position = "bottom",
    },
    -- This helps the menu show up faster
    delay = function(ctx)
      return ctx.plugin and 0 or 200
    end,
    spec = {
      -- Here we categorize your leader keymaps
      { "<leader>b", group = "Buffers", icon = "󰓩 " },
      { "<leader>f", group = "Find (Telescope)", icon = " " },
      { "<leader>g", group = "Git / Format", icon = "󰊢 " },
      { "<leader>s", group = "Splits", icon = " " },
      { "<leader>c", group = "Code / LSP", icon = " " },
      { "<leader>r", name = "Rename", icon = "󰑕 " },
    },
  }
}
