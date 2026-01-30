return {
  -- Mason package installer
  {
    "williamboman/mason.nvim",
    config = function()
      require("mason").setup()
    end,
  },
  -- Integration of Mason with nvim-lspconfig
  {
    "williamboman/mason-lspconfig.nvim",
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = {
          -- Web frameworks / Frontend:
          "angularls",            -- Angular
          "cssls",                -- CSS
          "html",                 -- HTML & HTMX (configured to include "htmx" filetype)
          "ts_ls",                -- TypeScript, JavaScript, React, etc.

          -- Scripting & Markup:
          "jsonls",               -- JSON/JSONC
          "marksman",             -- Markdown
          "yamlls",               -- YAML (used for Kubernetes files too)

          -- Backend & Systems:
          "clangd",               -- C and C++
          "omnisharp",            -- C#
          "jdtls",                -- Java
          "gopls",                -- Go
          "intelephense",         -- PHP (feature-rich)
          "pyright",              -- Python (including Django projects)
          "rust_analyzer",        -- Rust
          "sqlls",                -- SQL & Postgres

          -- Docker & DevOps:
          "dockerls",             -- Dockerfile
          "docker_compose_language_service", -- Docker Compose

          -- Additional Languages:
          --"dartls",               -- Dart
          "graphql",              -- GraphQL
          "lua_ls",               -- Lua
          "tinymist",             -- Typst
          "vuels",                -- Vue
          "lemminx",              -- XML 
        }
      })
    end,
  },
  -- nvim-lspconfig setup for language servers
  {
    "neovim/nvim-lspconfig",
    config = function()
      -- Common on_attach to map keybindings once LSP attaches to the buffer
      local on_attach = function(client, bufnr)
        local bufmap = function(mode, lhs, rhs, desc)
          vim.keymap.set(mode, lhs, rhs, { noremap = true, silent = true, buffer = bufnr, desc = desc })
        end
        bufmap("n", "K", vim.lsp.buf.hover, "LSP Hover")
        bufmap("n", "gd", vim.lsp.buf.definition, "LSP Definition")
        bufmap("n", "gi", vim.lsp.buf.implementation, "LSP Implementation")
        bufmap("n", "gr", vim.lsp.buf.references, "LSP References")
        bufmap({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, "LSP Code Action")
        bufmap("n", "<leader>rn", vim.lsp.buf.rename, "LSP Rename")

        -- Diagnostic keymaps
        bufmap("n", "[d", vim.diagnostic.goto_prev, "Previous Diagnostic")
        bufmap("n", "]d", vim.diagnostic.goto_next, "Next Diagnostic")
      end

      -- Setup capabilities (e.g., for nvim-cmp)
      local capabilities = vim.lsp.protocol.make_client_capabilities()
      local cmp_status, cmp_nvim_lsp = pcall(require, "cmp_nvim_lsp")
      if cmp_status then
        capabilities = cmp_nvim_lsp.default_capabilities(capabilities)
      end

      local lsp_servers = require("lspconfig")

      local default_servers = {
        "angularls", "cssls", "jsonls", "marksman", "clangd", "omnisharp",
        "jdtls", "gopls", "intelephense", "pyright", "rust_analyzer",
        "sqlls", "dockerls", "docker_compose_language_service",
        "graphql", "tinymist", "vuels", "lemminx"
      }

      for _, lsp in ipairs(default_servers) do
	vim.lsp.config(lsp, {
          on_attach = on_attach,
          capabilities = capabilities,
        })
	vim.lsp.enable(lsp)
      end

      -- HTML & HTMX
      vim.lsp.config("html", {
        filetypes = { "html", "htmx" },
        on_attach = on_attach,
        capabilities = capabilities,
      })
      vim.lsp.enable("html")

      -- TypeScript / JavaScript / React
      vim.lsp.config("ts_ls", {
        filetypes = { "javascript", "javascriptreact", "typescript", "typescriptreact" },
        on_attach = on_attach,
        capabilities = capabilities,
      })
      vim.lsp.enable("ts_ls")

      -- Lua (specifically for Neovim development)
      vim.lsp.config("lua_ls", {
        on_attach = on_attach,
        capabilities = capabilities,
        settings = {
          Lua = {
            diagnostics = { globals = { "vim" } },
            workspace = { checkThirdParty = false },
          },
        },
      })
      vim.lsp.enable("lua_ls")

      -- YAML / Kubernetes
      vim.lsp.config("yamlls", {
        on_attach = on_attach,
        capabilities = capabilities,
        settings = {
          yaml = {
            schemas = {
              kubernetes = "/*",
            },
          },
        },
      })
      vim.lsp.enable("yamlls")
    end,
  },
}

