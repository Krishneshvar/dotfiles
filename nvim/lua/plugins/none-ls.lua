return {
  "nvimtools/none-ls.nvim",

  config = function()
    local null_ls = require("null-ls")
    local formatting = null_ls.builtins.formatting
    local diagnostics = null_ls.builtins.diagnostics

    null_ls.setup({
      sources = {
        -- Formatters:
        formatting.stylua,         -- Lua
        formatting.prettier,         -- JavaScript, TypeScript, HTML, CSS, JSON, YAML, Markdown, Vue, etc.
        formatting.black,            -- Python
        formatting.gofumpt,          -- Go (better than gofmt)
        formatting.sqlfluff,         -- SQL & Postgres
        formatting.phpcbf,           -- PHP
        -- formatting.dart_format,      -- Dart
        -- (Omit C/C++ and Java formatters here so that you can rely on the native formatting provided by the LSP)

        -- Diagnostics:
        diagnostics.eslint_d,        -- JavaScript/TypeScript
        -- diagnostics.flake8,          -- Python
        diagnostics.golangci_lint,   -- Go
        diagnostics.phpcs,           -- PHP
        diagnostics.hadolint,        -- Docker
        diagnostics.yamllint,        -- YAML
      },
    })

    vim.keymap.set("n", "<leader>gf", vim.lsp.buf.format, {})
  end,
}

