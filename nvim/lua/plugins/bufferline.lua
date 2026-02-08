return {
  'akinsho/bufferline.nvim',
  config = function()
    require('bufferline').setup {
      options = {
        mode = 'buffers',
        style_preset = require('bufferline').style_preset.minimal,
        separator_style = "slant", -- Modern slanted look
        always_show_bufferline = true,
        show_buffer_close_icons = false,
        show_close_icon = false,
        indicator = { style = 'underline' },
        offsets = {
          {
            filetype = "neo-tree",
            text = "EXPLORER",
            text_align = "center",
            separator = true,
          }
        },
      }
    }
  end,
}
