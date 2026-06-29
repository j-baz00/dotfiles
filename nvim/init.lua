-- ~/.config/nvim/init.lua

-- Basic setup
vim.opt.nu = true             -- line numbers
vim.opt.relativenumber = true -- relative line numbers
vim.opt.tabstop = 2           -- sets tab to 2 spaces
vim.opt.shiftwidth = 2        -- number of spaces for each indentation
vim.opt.expandtab = true      -- spaces instead of tabs
vim.opt.smartindent = true
vim.opt.hlsearch = false      -- highlight search results off
vim.opt.softtabstop = 2

-- sets <Space>w to save file
vim.g.mapleader = ' '
vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save file" })

-- LazyVim setup
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable", -- latest stable release
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    -- Theme: GitHub Dark (matches the #0d1117 gray + bright accent palette)
    {
        "projekt0n/github-nvim-theme",
        name = "github-theme",
        lazy = false,    -- load during startup, it's the main UI plugin
        priority = 1000, -- load before everything else so highlights apply first
        config = function()
            require("github-theme").setup({
                options = {
                    transparent = false,
                    terminal_colors = false, -- set manually below to match Alacritty exactly
                    styles = {
                        comments = "italic",
                        keywords = "bold",
                        functions = "NONE",
                    },
                },
            })
        end,
    },

    {
        "nvim-tree/nvim-tree.lua",
        config = function()
            require("nvim-tree").setup()
        end,
    },

    {
        "nvim-treesitter/nvim-treesitter",
        build = ":TSUpdate",
        config = function()
            require("nvim-treesitter").setup({
                ensure_installed = { "lua", "python", "c", "cpp", "java" },
                auto_install = true,
                highlight = { enable = true },
                indent = { enable = true },
            })
        end
    },

    {
        "williamboman/mason.nvim",
        config = function()
            require("mason").setup()
        end
    },

    {
        "williamboman/mason-lspconfig.nvim",
        dependencies = { "williamboman/mason.nvim" },
        config = function()
            require("mason-lspconfig").setup({
                ensure_installed = { "lua_ls", "clangd", "jdtls", "pyright" },
                automatic_installation = true,
            })
        end
    },

    {
        "neovim/nvim-lspconfig",
        dependencies = { "williamboman/mason-lspconfig.nvim" },
        config = function()
            -- Lua LSP
            vim.lsp.config.lua_ls = {
                cmd = { "lua-language-server" },
                filetypes = { "lua" },
                root_markers = { ".luarc.json", ".luarc.jsonc", ".luacheckrc", ".stylua.toml", "stylua.toml", "selene.toml", ".git" },
                settings = {
                    Lua = {
                        runtime = { version = "LuaJIT" },
                        diagnostics = { globals = { "vim" } },
                    },
                },
            }

            -- C/C++ (clangd)
            vim.lsp.config.clangd = {
                cmd = { "clangd" },
                filetypes = { "c", "cpp", "objc", "objcpp" },
                root_markers = { ".clangd", ".clang-tidy", ".clang-format", "compile_commands.json", "CMakeLists.txt", ".git" },
            }

            -- Java (jdtls)
            vim.lsp.config.jdtls = {
                cmd = { "jdtls" },
                filetypes = { "java" },
                root_markers = { "gradlew", "mvnw", "build.gradle", "pom.xml", ".git" },
            }

            -- Python (pyright)
            vim.lsp.config.pyright = {
                cmd = { "pyright-langserver", "--stdio" },
                filetypes = { "python" },
                root_markers = { "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "Pipfile", ".git" },
            }

            -- Enable LSP servers
            vim.lsp.enable("lua_ls")
            vim.lsp.enable("clangd")
            vim.lsp.enable("jdtls")
            vim.lsp.enable("pyright")
        end,
    },
})

-- Set colorscheme after plugins are loaded.
-- github_dark_dimmed (#22272e) matches the Alacritty github_dark slate (#24292e).
vim.cmd.colorscheme("github_dark_dimmed")

-- Make Neovim's built-in :terminal use the exact Alacritty github_dark palette,
-- so an embedded terminal looks identical to the host terminal.
local alacritty_github_dark = {
    [0]  = "#586069", -- black
    [1]  = "#ea4a5a", -- red
    [2]  = "#34d058", -- green
    [3]  = "#ffea7f", -- yellow
    [4]  = "#2188ff", -- blue
    [5]  = "#b392f0", -- magenta
    [6]  = "#39c5cf", -- cyan
    [7]  = "#d1d5da", -- white
    [8]  = "#959da5", -- bright black
    [9]  = "#f97583", -- bright red
    [10] = "#85e89d", -- bright green
    [11] = "#ffea7f", -- bright yellow
    [12] = "#79b8ff", -- bright blue
    [13] = "#b392f0", -- bright magenta
    [14] = "#56d4dd", -- bright cyan
    [15] = "#fafbfc", -- bright white
}
for i, hex in pairs(alacritty_github_dark) do
    vim.g["terminal_color_" .. i] = hex
end
vim.keymap.set("n", "<leader>e", ":NvimTreeToggle<CR>") -- Toggle file explorer

-- LSP keybinds
vim.api.nvim_create_autocmd('LspAttach', {
    group = vim.api.nvim_create_augroup('UserLspConfig', {}),
    callback = function(ev)
        local opts = { buffer = ev.buf }
        vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
        vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
        vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
        vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
        vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
        vim.keymap.set('n', '<leader>f', vim.lsp.buf.format, opts) -- Auto-format file
    end,
})
