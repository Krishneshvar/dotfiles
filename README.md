# dotfiles
All my linux configuration files

## Automated Installation
An installation script is provided to automatically create symlinks for your user configurations and copy system-wide preferences, creating backups of any existing folders/files.

1. Clone the repository
2. Change into the directory: `cd dotfiles`
3. Run the installer script: `./install.sh`

## Manual Installation
- Clone the repository
- The following are to be placed in the `~/.config/` folder:
  - [hypr](./hypr/)
  - [kitty](./kitty/)
  - [matugen](./matugen/)
  - [nvim](./nvim/)
  - [rofi](./rofi/)
  - [swaync](./swaync/)
  - [swayosd](./swayosd/)
  - [wallengine](./wallengine/)
  - [waybar](./waybar/)
  - [starship](./starship.toml)

- [.zshrc](./.zshrc) should be placed in `~`
