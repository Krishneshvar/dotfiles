return {
  -- Auto-close brackets/quotes
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    config = true
  },
  -- Auto-close & rename HTML tags (Essential for your React work)
  {
    "windwp/nvim-ts-autotag",
    ft = { "html", "javascript", "typescript", "javascriptreact", "typescriptreact", "xml" },
    config = function()
      require('nvim-ts-autotag').setup()
    end
  }
}
