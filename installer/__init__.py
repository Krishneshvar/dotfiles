"""
Installer package for Hyprland dotfiles.
"""

from installer.configs import setup_user_configs
from installer.packages import (
    CONFIG_AUR,
    CONFIG_PACMAN,
    EXTRA_AUR,
    EXTRA_PACMAN,
    install_packages,
)
from installer.system import setup_system_wide
from installer.ui import (
    Style,
    box_print,
    error,
    info,
    section,
    success,
    warn,
)

__all__ = [
    "Style",
    "box_print",
    "section",
    "info",
    "success",
    "warn",
    "error",
    "CONFIG_PACMAN",
    "CONFIG_AUR",
    "EXTRA_PACMAN",
    "EXTRA_AUR",
    "install_packages",
    "setup_user_configs",
    "setup_system_wide",
]
