#!/usr/bin/env bash
set -e

# Path to the directory where this script resides
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Network check function
check_network() {
    ping -c 1 -W 2 1.1.1.1 >/dev/null 2>&1 || \
    ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1 || \
    (command -v curl >/dev/null 2>&1 && curl -s --connect-timeout 3 https://archlinux.org >/dev/null 2>&1) || \
    (command -v wget >/dev/null 2>&1 && wget -q --spider --timeout=3 https://archlinux.org >/dev/null 2>&1)
}

# Check network connectivity before starting (skip for offline flags)
SKIP_NET=0
for arg in "$@"; do
    if [ "$arg" = "--config-only" ] || [ "$arg" = "--dry-run" ]; then
        SKIP_NET=1
        break
    fi
done

if [ "$SKIP_NET" -eq 0 ]; then
    if ! check_network; then
        echo -e "\033[38;2;243;139;168m\033[1m✗ Error: No internet connection detected.\033[0m"
        echo "An active internet connection is required for installation. Please connect and retry."
        exit 1
    fi
fi

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
