vim.api.nvim_create_autocmd("FileType", {
  pattern = "markdown",
  callback = function()
    vim.opt_local.wrap = true
    vim.opt_local.spell = true
    vim.opt_local.spelllang = "en,de"
    vim.opt_local.linebreak = true
    vim.opt_local.conceallevel = 2
  end,
})
