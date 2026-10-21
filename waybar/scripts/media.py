#!/usr/bin/env python3
"""
Robust Waybar Media Player Module using Playerctl
Outputs JSON stream for Waybar's custom module without risking in-process C++ crashes.
"""

import sys
import json
import html
import signal

try:
    import gi
    gi.require_version("Playerctl", "2.0")
    from gi.repository import Playerctl, GLib
except Exception as e:
    sys.stderr.write(f"Playerctl or PyGObject not found: {e}\n")
    sys.exit(1)

PLAYER_ICONS = {
    "spotify": " ",
    "firefox": "󰈹 ",
    "chromium": " ",
    "chrome": " ",
    "brave": "󰈹 ",
    "vlc": "󰕼 ",
    "mpv": "󰐌 ",
    "default": " "
}

def get_player_icon(player_name):
    lower = (player_name or "").lower()
    for key, icon in PLAYER_ICONS.items():
        if key in lower:
            return icon
    return PLAYER_ICONS["default"]

def emit_status(player=None):
    if not player:
        sys.stdout.write(json.dumps({"text": "", "class": "stopped"}) + "\n")
        sys.stdout.flush()
        return

    try:
        status = player.props.playback_status
    except Exception:
        status = Playerctl.PlaybackStatus.STOPPED

    if status == Playerctl.PlaybackStatus.STOPPED:
        sys.stdout.write(json.dumps({"text": "", "class": "stopped"}) + "\n")
        sys.stdout.flush()
        return

    try:
        title = player.get_title() or ""
        artist = player.get_artist() or ""
        album = player.get_album() or ""
        name = player.props.player_name or "Media"
    except Exception:
        title, artist, album, name = "", "", "", "Media"

    if not title and not artist:
        sys.stdout.write(json.dumps({"text": "", "class": "stopped"}) + "\n")
        sys.stdout.flush()
        return

    icon = get_player_icon(name)
    if artist and title:
        raw_text = f"{artist} — {title}"
    else:
        raw_text = title or artist

    max_len = 32
    if len(raw_text) > max_len:
        display_text = raw_text[:max_len - 1] + "…"
    else:
        display_text = raw_text

    escaped = html.escape(display_text)
    is_paused = (status == Playerctl.PlaybackStatus.PAUSED)
    status_str = getattr(status, "value_nick", "Paused" if is_paused else "Playing")

    if is_paused:
        formatted_text = f"{icon}<i>{escaped}</i>"
        css_class = "paused"
    else:
        formatted_text = f"{icon}{escaped}"
        css_class = "playing"

    tooltip_lines = [f"{name} ({status_str})", raw_text]
    if album:
        tooltip_lines.append(album)

    payload = {
        "text": formatted_text,
        "alt": name,
        "tooltip": "\n".join(tooltip_lines),
        "class": css_class
    }

    try:
        sys.stdout.write(json.dumps(payload) + "\n")
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        sys.exit(0)

class MediaWatcher:
    def __init__(self):
        self.manager = Playerctl.PlayerManager()
        self.loop = GLib.MainLoop()
        self.players = {}

        self.manager.connect("name-appeared", self.on_name_appeared)
        self.manager.connect("player-vanished", self.on_player_vanished)

        for player_name in self.manager.props.player_names:
            self.add_player(player_name)

        self.refresh()

    def add_player(self, name):
        try:
            player_str = name.name if hasattr(name, "name") else str(name)
            if "playerctld" in player_str.lower():
                return
            player = Playerctl.Player.new_from_name(name)
            player.connect("playback-status", lambda p, s: self.refresh())
            player.connect("metadata", lambda p, m: self.refresh())
            self.manager.manage_player(player)
            self.players[player.props.player_name] = player
        except Exception:
            pass

    def on_name_appeared(self, manager, name):
        self.add_player(name)
        self.refresh()

    def on_player_vanished(self, manager, player):
        try:
            name = player.props.player_name
            if name in self.players:
                del self.players[name]
        except Exception:
            pass
        self.refresh()

    def refresh(self):
        active = None
        # Prefer Playing player, fallback to Paused
        for p in list(self.players.values()):
            try:
                st = p.props.playback_status
                if st == Playerctl.PlaybackStatus.PLAYING:
                    active = p
                    break
                elif st == Playerctl.PlaybackStatus.PAUSED and not active:
                    active = p
            except Exception:
                continue

        emit_status(active)

    def run(self):
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
        try:
            self.loop.run()
        except (KeyboardInterrupt, SystemExit):
            pass

if __name__ == "__main__":
    watcher = MediaWatcher()
    watcher.run()
