#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GtkLayerShell, GLib
import os
import sys
import calendar
from datetime import datetime

class CustomCalendar(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(16)
        
        self.today = datetime.now()
        self.view_month = self.today.month
        self.view_year = self.today.year
        
        # Header Box
        header = Gtk.Box()
        header.set_orientation(Gtk.Orientation.HORIZONTAL)
        header.set_spacing(0)
        header.set_name("calendar-header")
        
        # Month Navigation
        self.prev_btn = Gtk.Button.new_from_icon_name("pan-start-symbolic", Gtk.IconSize.BUTTON)
        self.next_btn = Gtk.Button.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON)
        self.prev_btn.connect("clicked", lambda x: self.change_month(-1))
        self.next_btn.connect("clicked", lambda x: self.change_month(1))
        
        self.month_label = Gtk.Label()
        self.month_label.set_name("month-label")
        self.month_label.set_hexpand(True)
        self.month_label.set_halign(Gtk.Align.CENTER)
        
        header.pack_start(self.prev_btn, False, False, 0)
        header.pack_start(self.month_label, True, True, 0)
        header.pack_start(self.next_btn, False, False, 0)
        
        self.pack_start(header, False, False, 0)
        
        # Year Navigation (Subtle)
        year_box = Gtk.Box()
        year_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        year_box.set_spacing(8)
        year_box.set_halign(Gtk.Align.CENTER)
        
        self.prev_year = Gtk.Button.new_from_icon_name("pan-start-symbolic", Gtk.IconSize.MENU)
        self.next_year = Gtk.Button.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.MENU)
        self.prev_year.connect("clicked", lambda x: self.change_year(-1))
        self.next_year.connect("clicked", lambda x: self.change_year(1))
        
        self.prev_year.get_style_context().add_class("year-btn")
        self.next_year.get_style_context().add_class("year-btn")
        
        self.year_label = Gtk.Label()
        self.year_label.set_name("year-label")
        
        year_box.pack_start(self.prev_year, False, False, 0)
        year_box.pack_start(self.year_label, False, False, 0)
        year_box.pack_start(self.next_year, False, False, 0)
        
        self.pack_start(year_box, False, False, 0)

        # The Grid
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(6)
        self.grid.set_row_spacing(6)
        self.grid.set_halign(Gtk.Align.CENTER)
        # Make the grid homogeneous so the numbers perfectly align like a matrix
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.pack_start(self.grid, True, True, 0)
        
        self.update_calendar()

    def change_month(self, delta):
        self.view_month += delta
        if self.view_month > 12:
            self.view_month = 1
            self.view_year += 1
        elif self.view_month < 1:
            self.view_month = 12
            self.view_year -= 1
        self.update_calendar()

    def change_year(self, delta):
        self.view_year += delta
        self.update_calendar()

    def update_calendar(self):
        for child in self.grid.get_children():
            self.grid.remove(child)
            
        self.month_label.set_text(calendar.month_name[self.view_month])
        self.year_label.set_text(str(self.view_year))
        
        # Weekday headers 
        days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        for i, day in enumerate(days):
            lbl = Gtk.Label(label=day)
            lbl.get_style_context().add_class("day-header")
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.set_valign(Gtk.Align.CENTER)
            self.grid.attach(lbl, i, 0, 1, 1)
            
        cal = calendar.Calendar(calendar.SUNDAY)
        month_days = cal.monthdays2calendar(self.view_year, self.view_month)
        
        prev_month = self.view_month - 1 or 12
        prev_year = self.view_year if self.view_month > 1 else self.view_year - 1
        prev_month_len = calendar.monthrange(prev_year, prev_month)[1]
        
        # First week padding
        first_week = month_days[0]
        padding = 0
        for i, (day, _) in enumerate(first_week):
            if day == 0: padding += 1
            else: break
            
        for i in range(padding):
            day_val = prev_month_len - padding + i + 1
            lbl = Gtk.Label(label=str(day_val))
            lbl.get_style_context().add_class("other-month")
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.set_valign(Gtk.Align.CENTER)
            self.grid.attach(lbl, i, 1, 1, 1)

        # Current month
        row = 1
        for week in month_days:
            for i, (day, _) in enumerate(week):
                if day == 0: continue # This skips drawing days outside the current month
                
                lbl = Gtk.Label(label=str(day))
                ctx = lbl.get_style_context()
                lbl.set_halign(Gtk.Align.CENTER)
                lbl.set_valign(Gtk.Align.CENTER)
                
                if (day == self.today.day and 
                    self.view_month == self.today.month and 
                    self.view_year == self.today.year):
                    ctx.add_class("today")
                else:
                    ctx.add_class("current-month")
                
                self.grid.attach(lbl, i, row, 1, 1)
            row += 1

        self.show_all()

class CalendarWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Calendar")
        
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        
        # Position: Top-Left anchoring
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        
        # Position Margins: 4px from Waybar, 10px from the left screen edge
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 4)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, 10)
        
        # Enable on-demand keyboard focus to capture clicks outside the window
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.ON_DEMAND)
        
        self.setup_css()
        
        card = Gtk.Box()
        card.set_orientation(Gtk.Orientation.VERTICAL)
        card.set_name("calendar-card")
        self.add(card)
        
        self.cal = CustomCalendar()
        card.pack_start(self.cal, True, True, 0)
        
        # Bind the focus-out event to the close function
        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_key_press)
        
        self.show_all()
        # Force the window to present itself and grab focus immediately
        self.present()

    def setup_css(self):
        css_provider = Gtk.CssProvider()
        matugen_colors_path = os.path.expanduser("~/.config/matugen/generated/colors.css")
        
        try:
            with open(matugen_colors_path, "r") as f:
                colors_css = f.read()
        except:
            colors_css = ""

        custom_css = f"""
        {colors_css}
        
        window {{
            background: transparent;
        }}
        
        #calendar-card {{
            background-color: @bg;
            border: 1px solid @outline;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        label {{
            font-family: "JetBrainsMono Nerd Font", Roboto, sans-serif;
        }}
        
        #month-label {{
            font-size: 16px;
            font-weight: 800;
            color: @fg;
        }}
        
        #year-label {{
            font-size: 13px;
            font-weight: 600;
            color: @fg_muted;
        }}
        
        .day-header {{
            font-size: 12px;
            font-weight: 700;
            color: @accent;
            padding-bottom: 8px;
        }}
        
        /* Fixed sizing for the grid cells ensures perfectly aligned numbers */
        .current-month, .other-month, .today {{
            min-width: 32px;
            min-height: 32px;
            padding: 0;
        }}
        
        .current-month {{
            font-size: 13px;
            font-weight: 500;
            color: @fg;
        }}
        
        .other-month {{
            font-size: 13px;
            font-weight: 500;
            color: alpha(@fg_muted, 0.4);
        }}
        
        .today {{
            font-size: 13px;
            font-weight: 700;
            color: @accent_fg;
            background-color: @accent;
            border-radius: 99px; /* Maps to a perfect circle because of fixed sizing */
        }}
        
        button {{
            color: @fg;
            background: transparent;
            border: none;
            border-radius: 99px;
            padding: 6px;
            min-width: 28px;
            min-height: 28px;
            transition: all 0.2s ease;
        }}
        
        button:hover {{
            background-color: @bg_alt;
            color: @accent;
        }}
        
        button.year-btn {{
            padding: 4px;
            min-width: 24px;
            min-height: 24px;
            color: @fg_muted;
        }}
        
        button.year-btn:hover {{
            color: @fg;
        }}
        """
        
        css_provider.load_from_data(custom_css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_focus_out(self, widget, event):
        self.close_and_exit()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.close_and_exit()

    def close_and_exit(self):
        self.destroy()
        Gtk.main_quit()
        sys.exit(0)

if __name__ == "__main__":
    win = CalendarWindow()
    Gtk.main()
