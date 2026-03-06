#!/usr/bin/env bash

# CPU EPP
echo balance_performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference

# allow full turbo
echo 100 | sudo tee /sys/devices/system/cpu/intel_pstate/max_perf_pct

# enable animations
hyprctl keyword animations:enabled true

notify-send "Power Mode" "Performance mode enabled"
