return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  lazy = false,
  config = function()
    local status, treesitter = pcall(require, "nvim-treesitter.configs")
    if not status then
        print("Treesitter configuration could not be loaded!")
        return
    end

    treesitter.setup({
      ensure_installed = {
        "angular",
        "arduino",
        "asm",
        "bash",
        "c",
        "cpp",
        "css",
        "csv",
        "dart",
        "dockerfile",
        "go",
        "html",
        "htmldjango",
        "java",
        "javascript",
        "json",
        "json5",
        "lua",
        "nginx",
        "php",
        "python",
        "rust",
        "sql",
        "tsx",
        "typescript",
        "typst",
        "vim",
        "vue",
        "xml",
        "yaml",
      },
      -- Use the line below if you want Treesitter to automatically install a new parser based on the file
      -- auto_install = true,
      highlight = { enable = true },
      indent = { enable = true },
    })
  end,
}

