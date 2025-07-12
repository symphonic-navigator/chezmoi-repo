#! /bin/bash

set -e
set -u

if ! echo "$XDG_CURRENT_DESKTOP" | grep -qi "hyprland"; then
  echo "❌ not on hyprland, exiting."
  exit 1
fi

IS_LAPTOP=false
if ls /sys/class/power_supply/ | grep -qi BAT; then
  IS_LAPTOP=true
fi

# --- This will be useful for all setups anyway ---
systemctl --user daemon-reexec
systemctl --user daemon-reload

# --- Common Setup ---
# todo: add hyprland setup for all kits here
echo "✅ common hyprland setup."

if [[ "$IS_LAPTOP" == false ]]; then
  echo "ℹ️ not a laptop, exiting."
  exit 2
fi

# --- Laptop Setup ---
systemctl --user enable --now hyprland-laptop-controller.timer
echo "✅ hyprland laptop setup successfully established."
