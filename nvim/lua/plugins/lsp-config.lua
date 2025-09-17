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
          "rust_analyzer", "rustup",-- Rust
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
      local capabilities = require('cmp_nvim_lsp').default_capabilities()
      local cmp_status, cmp_nvim_lsp = pcall(require, "cmp_nvim_lsp")
      if cmp_status then
        capabilities = cmp_nvim_lsp.default_capabilities(capabilities)
      end

      local lspconfig = require("lspconfig")

      -- Frontend/JS ecosystem:
      lspconfig.angularls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.cssls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.html.setup({
        filetypes = { "html", "htmx" },
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.ts_ls.setup({
        filetypes = { "javascript", "javascriptreact", "javascript.jsx", "typescript", "typescriptreact", "typescript.tsx" },
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.jsonls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })

      -- Backend, systems, and general-purpose languages:
      lspconfig.clangd.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.omnisharp.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.jdtls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.gopls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.intelephense.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.pyright.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.rust_analyzer.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.sqlls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })

      -- Docker/DevOps:
      lspconfig.dockerls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.docker_compose_language_service.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })

      -- Other ecosystems:
      --lspconfig.dartls.setup({
      --  on_attach = on_attach,
      --  capabilities = capabilities,
      --})
      lspconfig.graphql.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.lua_ls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
        settings = {
          Lua = {
            diagnostics = { globals = { "vim" } },
            workspace = { checkThirdParty = false },
          },
        },
      })
      lspconfig.tinymist.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.vuels.setup({
        on_attach = on_attach,
       capabilities = capabilities,
      })
      lspconfig.lemminx.setup({
        on_attach = on_attach,
        capabilities = capabilities,
      })
      lspconfig.yamlls.setup({
        on_attach = on_attach,
        capabilities = capabilities,
        settings = {
          yaml = {
            schemas = {
              kubernetes = "/*",  -- Adjust this schema mapping per project as needed
            },
          },
        },
      })
    end,
  },
}

