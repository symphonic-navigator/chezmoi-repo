vim.api.nvim_create_user_command("PandocPreview", function()
  local filepath = vim.fn.expand("%:p")
  local tmpfile = "/tmp/preview.html"
  local cmd = string.format("pandoc '%s' -o '%s'", filepath, tmpfile)
  vim.fn.system(cmd)
  vim.fn.jobstart({ "xdg-open", tmpfile }, { detach = true })
end, { desc = "Render to HTML and preview in browser" })
