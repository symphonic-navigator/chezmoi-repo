-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--
vim.keymap.set("n", "<leader>mp", ":PandocPreview<CR>", { desc = "Preview render in browser" })

vim.keymap.set("n", "ö", ":", { noremap = true })
vim.keymap.set("v", "ö", ":", { noremap = true })

vim.keymap.set("n", "-", "/", { noremap = true })
vim.keymap.set("v", "-", "/", { noremap = true })

vim.keymap.set("n", "_", "?", { noremap = true })
vim.keymap.set("v", "_", "?", { noremap = true })
