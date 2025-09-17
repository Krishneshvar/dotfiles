-- BASIC SETTINGS
vim.cmd("set nocompatible")             -- Disable Vi compatibility
vim.opt.encoding = "utf-8"              -- Use UTF-8 encoding
vim.opt.fileencoding = "utf-8"          -- File content encoding for current buffer

-- INDENTATION
vim.opt.expandtab = true                -- Convert tabs to spaces
vim.opt.tabstop = 2                     -- Number of spaces that a <Tab> counts for
vim.opt.softtabstop = 2                 -- Number of spaces when pressing Tab in insert mode
vim.opt.shiftwidth = 2                  -- Number of spaces for autoindent
vim.opt.smarttab = true                 -- Makes tabbing smarter
vim.opt.autoindent = true               -- Copy indent from current line when starting a new one
vim.opt.smartindent = true              -- Smarter autoindentation (e.g. in code blocks)

-- LINE NUMBERS
vim.wo.number = true                    -- Show line numbers
vim.wo.relativenumber = true           -- Show relative line numbers (set to true if you want them)

-- SEARCH
vim.opt.hlsearch = true                 -- Highlight search results
vim.opt.incsearch = true                -- Show search matches as you type
vim.opt.ignorecase = true              -- Ignore case when searching
vim.opt.smartcase = true               -- Override ignorecase if search has uppercase letters

-- UI
vim.opt.termguicolors = true            -- Enable 24-bit RGB colors
vim.opt.cursorline = true               -- Highlight the current line
vim.opt.scrolloff = 8                   -- Keep 8 lines visible above/below the cursor
vim.opt.sidescrolloff = 8               -- Keep 8 columns visible on the sides
vim.opt.signcolumn = "yes"              -- Always show the sign column (useful for Git/Gutter)
vim.opt.wrap = false                    -- Disable line wrapping
-------------------------------------------------------------------------------------------------------------------------------------------------------------

-- BACKUPS & SWAPS
vim.opt.swapfile = false                -- Disable swap file
vim.opt.backup = false                  -- Disable backup file
vim.opt.undofile = true                 -- Enable persistent undo

-- MOUSE & CLIPBOARD
vim.opt.mouse = "a"                     -- Enable mouse support
vim.opt.clipboard = "unnamedplus"      -- Use system clipboard

-- COMPLETION
vim.opt.wildmenu = true                 -- Enhanced command-line completion
vim.opt.completeopt = { "menuone", "noselect" }  -- Better completion experience

-- SPLITS
vim.opt.splitright = true               -- Vertical splits open to the right
vim.opt.splitbelow = true               -- Horizontal splits open below

-- PERFORMANCE
vim.opt.updatetime = 300                -- Faster completion (default is 4000ms)
vim.opt.timeoutlen = 500                -- Time to wait for a mapped sequence

-- MISC
vim.g.mapleader = " "                   -- Set <Space> as leader key
vim.opt.hidden = true                   -- Allow buffer switching without saving
vim.opt.backspace = { "indent", "eol", "start" }  -- Make backspace behave like in modern editors
vim.opt.history = 1000                  -- Number of lines to keep in command-line history

-- FOLDING
vim.opt.foldmethod = "marker"           -- Folding method: manual, indent, syntax, expr, marker
vim.opt.foldlevel = 99                  -- Open all folds by default

-- GUI ONLY (if using Neovide or GUI client)
-- vim.opt.guifont = "JetBrainsMono Nerd Font:h14" -- GUI font (adjust for your system)

