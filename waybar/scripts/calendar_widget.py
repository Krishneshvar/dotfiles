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
        self.set_spacing(15)
        
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
        
        header.pack_start(self.prev_btn, False, False, 0)
        header.pack_start(self.month_label, True, True, 0)
        header.pack_start(self.next_btn, False, False, 0)
        
        self.pack_start(header, False, False, 0)
        
        # Year Navigation (Subtle)
        year_box = Gtk.Box()
        year_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        year_box.set_spacing(5)
        year_box.set_halign(Gtk.Align.CENTER)
        
        self.prev_year = Gtk.Button.new_from_icon_name("pan-start-symbolic", Gtk.IconSize.MENU)
        self.next_year = Gtk.Button.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.MENU)
        self.prev_year.connect("clicked", lambda x: self.change_year(-1))
        self.next_year.connect("clicked", lambda x: self.change_year(1))
        
        self.year_label = Gtk.Label()
        self.year_label.set_name("year-label")
        
        year_box.pack_start(self.prev_year, False, False, 0)
        year_box.pack_start(self.year_label, False, False, 0)
        year_box.pack_start(self.next_year, False, False, 0)
        
        self.pack_start(year_box, False, False, 0)

        # The Grid
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.grid.set_halign(Gtk.Align.CENTER)
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
        # Clear specific grid children
        for child in self.grid.get_children():
            self.grid.remove(child)
            
        self.month_label.set_text(calendar.month_name[self.view_month])
        self.year_label.set_text(str(self.view_year))
        
        # Weekday headers
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            lbl = Gtk.Label(label=day)
            lbl.get_style_context().add_class("day-header")
            self.grid.attach(lbl, i, 0, 1, 1)
            
        # Get calendar data
        cal = calendar.Calendar(calendar.SUNDAY)
        month_days = cal.monthdays2calendar(self.view_year, self.view_month)
        
        # Calculate context for other months
        prev_month = self.view_month - 1 or 12
        prev_year = self.view_year if self.view_month > 1 else self.view_year - 1
        prev_month_len = calendar.monthrange(prev_year, prev_month)[1]
        
        r = 1
        # We need to fill the grid with exactly 6 weeks for consistency
        all_days = cal.monthdays2calendar(self.view_year, self.view_month)
        
        # First week might have leading 0s
        first_week = all_days[0]
        padding = 0
        for i, (day, _) in enumerate(first_week):
            if day == 0: padding += 1
            else: break
            
        # Draw padding from previous month
        for i in range(padding):
            day_val = prev_month_len - padding + i + 1
            lbl = Gtk.Label(label=str(day_val))
            lbl.get_style_context().add_class("other-month")
            self.grid.attach(lbl, i, 1, 1, 1)

        # Draw current month and remaining padding
        row = 1
        for week in all_days:
            for i, (day, _) in enumerate(week):
                if day == 0: continue
                
                lbl = Gtk.Label(label=str(day))
                ctx = lbl.get_style_context()
                
                if (day == self.today.day and 
                    self.view_month == self.today.month and 
                    self.view_year == self.today.year):
                    ctx.add_class("today")
                else:
                    ctx.add_class("current-month")
                
                self.grid.attach(lbl, i, row, 1, 1)
            row += 1
            
        # Fill training padding for next month
        last_week = all_days[-1]
        next_padding = 0
        filling = False
        next_day = 1
        
        # If we have less than 6 rows, keep adding
        while row <= 6:
            for i in range(7):
                # Check if this cell is already occupied
                if self.grid.get_child_at(i, row) is None:
                    lbl = Gtk.Label(label=str(next_day))
                    lbl.get_style_context().add_class("other-month")
                    self.grid.attach(lbl, i, row, 1, 1)
                    next_day += 1
            row += 1

        self.show_all()

class CalendarWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Calendar")
        
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 4)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        
        self.setup_css()
        
        card = Gtk.Box()
        card.set_orientation(Gtk.Orientation.VERTICAL)
        card.set_name("calendar-card")
        self.add(card)
        
        self.cal = CustomCalendar()
        card.pack_start(self.cal, True, True, 0)
        
        self.connect("focus-out-event", lambda w, e: self.close_and_exit())
        self.connect("key-press-event", self.on_key_press)
        
        self.show_all()

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
        
        window {{ background: transparent; }}
        
        #calendar-card {{
            background-color: @bg_alt;
            border: 1px solid @outline;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        label {{
            font-family: "JetBrainsMono Nerd Font", monospace;
            font-weight: bold;
        }}
        
        #month-label {{
            font-size: 16px;
            color: @accent;
        }}
        
        #year-label {{
            font-size: 13px;
            color: alpha(@accent, 0.6);
        }}
        
        .day-header {{
            font-size: 12px;
            color: @accent;
            padding: 5px;
            margin-bottom: 5px;
        }}
        
        .current-month {{
            font-size: 14px;
            color: @fg;
            padding: 8px;
            min-width: 35px;
        }}
        
        .other-month {{
            font-size: 14px;
            color: alpha(@fg_muted, 0.25);
            padding: 8px;
            min-width: 35px;
        }}
        
        .today {{
            font-size: 14px;
            color: @accent_fg;
            background-color: @accent;
            border-radius: 8px;
            padding: 8px;
            min-width: 35px;
        }}
        
        button {{
            color: @accent;
            background: transparent;
            border: none;
            border-radius: 50%;
            padding: 5px;
        }}
        
        button:hover {{
            background-color: alpha(@accent, 0.15);
        }}
        """
        
        css_provider.load_from_data(custom_css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

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
