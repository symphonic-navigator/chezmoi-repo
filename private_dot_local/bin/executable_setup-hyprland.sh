#! /bin/bash

set -e
set -u

IS_LAPTOP=false
if ls /sys/class/power_supply/ | grep -qi BAT; then
  IS_LAPTOP=true
fi

IS_HYPRLAND=false
if echo "$XDG_CURRENT_DESKTOP" | grep -qi "hyprland"; then
  IS_HYPRLAND=true
fi

if [[ "$IS_HYPRLAND" == false ]]; then
  echo "❌ not on hyprland, exiting."
  exit 1
fi

if [[ "$IS_LAPTOP" == false ]]; then
  echo "❌ not a laptop, exiting."
  exit 2
fi

systemctl --user enable lid-robot.timer
echo "✅ hyprland laptop setup successfully established."
