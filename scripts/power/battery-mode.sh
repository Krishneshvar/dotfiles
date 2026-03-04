#!/usr/bin/env bash

# CPU EPP
echo power | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference

# Reduce Intel boost aggressiveness
echo 70 | sudo tee /sys/devices/system/cpu/intel_pstate/max_perf_pct

# Hyprland animations reduced
hyprctl keyword animations:enabled false

notify-send "Power Mode" "Battery mode enabled"
