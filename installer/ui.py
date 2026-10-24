"""
UI utilities and terminal styling for the dotfiles installer.
"""

import sys


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Modern Palette
    BLUE = "\033[38;2;137;180;250m"       # #89b4fa
    MAUVE = "\033[38;2;203;166;247m"      # #cba6f7
    CYAN = "\033[38;2;137;220;235m"       # #89dceb
    GREEN = "\033[38;2;166;227;161m"      # #a6e3a1
    YELLOW = "\033[38;2;249;226;175m"     # #f9e2af
    PEACH = "\033[38;2;250;179;135m"      # #fab387
    RED = "\033[38;2;243;139;168m"        # #f38ba8
    GRAY = "\033[38;2;108;112;134m"       # #6c7086
    WHITE = "\033[38;2;205;214;244m"      # #cdd6f4


def box_print(title: str, subtitle: str = ""):
    width = 68
    print(f"\n{Style.MAUVE}╭{'─' * (width - 2)}╮{Style.RESET}")
    print(f"{Style.MAUVE}│{Style.RESET}{Style.BOLD}{Style.WHITE}{title.center(width - 2)}{Style.RESET}{Style.MAUVE}│{Style.RESET}")
    if subtitle:
        print(f"{Style.MAUVE}│{Style.RESET}{Style.CYAN}{subtitle.center(width - 2)}{Style.RESET}{Style.MAUVE}│{Style.RESET}")
    print(f"{Style.MAUVE}╰{'─' * (width - 2)}╯{Style.RESET}\n")


def section(step: str, title: str):
    print(f"\n{Style.BOLD}{Style.BLUE}◆ [{step}] {Style.WHITE}{title}{Style.RESET}")
    print(f"{Style.GRAY}{'─' * 60}{Style.RESET}")


def info(msg: str):
    print(f"  {Style.CYAN}ℹ{Style.RESET} {msg}")


def success(msg: str):
    print(f"  {Style.GREEN}✓{Style.RESET} {msg}")


def warn(msg: str):
    print(f"  {Style.YELLOW}⚠{Style.RESET} {msg}")


def error(msg: str):
    print(f"  {Style.RED}✗{Style.RESET} {msg}")


def alert(title: str, message: str):
    import textwrap
    width = 68
    inner_width = width - 4
    content_width = inner_width - 2
    print(f"\n  {Style.BOLD}{Style.RED}┌{'─' * inner_width}┐{Style.RESET}")
    header_text = f"⚠ ALERT: {title}"
    pad = inner_width - len(header_text) - 2
    print(f"  {Style.BOLD}{Style.RED}│ {header_text}" + " " * max(0, pad) + f" │{Style.RESET}")
    print(f"  {Style.BOLD}{Style.RED}├{'─' * inner_width}┤{Style.RESET}")
    for raw_line in message.strip().splitlines():
        if not raw_line.strip():
            print(f"  {Style.BOLD}{Style.RED}│{Style.RESET}" + " " * (inner_width) + f"{Style.BOLD}{Style.RED}│{Style.RESET}")
            continue
        wrapped = [raw_line] if raw_line.startswith("  •") else textwrap.wrap(raw_line, content_width)
        for line in wrapped:
            l_pad = content_width - len(line)
            print(f"  {Style.BOLD}{Style.RED}│{Style.RESET} {Style.WHITE}{line}" + " " * max(0, l_pad) + f" {Style.BOLD}{Style.RED}│{Style.RESET}")
    print(f"  {Style.BOLD}{Style.RED}└{'─' * inner_width}┘{Style.RESET}\n")


def prompt_input(prompt_text: str, default: str = "") -> str:
    try:
        val = input(f"  {Style.BOLD}{Style.MAUVE}{prompt_text}{Style.RESET}").strip()
        return val if val else default
    except (KeyboardInterrupt, EOFError):
        print("\nAborted by user.")
        sys.exit(0)
