#!/usr/bin/env bash
set -e

# Path to the directory where this script resides
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure bootstrap prerequisites (git and python) are installed
MISSING_PKGS=()
command -v git >/dev/null 2>&1 || MISSING_PKGS+=(git)
command -v python3 >/dev/null 2>&1 || MISSING_PKGS+=(python)

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo "--> Installing bootstrap prerequisites: ${MISSING_PKGS[*]}..."
    if command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --needed --noconfirm "${MISSING_PKGS[@]}"
    else
        echo "Error: pacman not found. Please install ${MISSING_PKGS[*]} manually."
        exit 1
    fi
fi

# Automatically hand over to the Python installer
exec python3 "$DOTFILES_DIR/install.py" "$@"
