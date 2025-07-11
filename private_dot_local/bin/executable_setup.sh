#! /bin/bash

IS_LAPTOP=false
if ls /sys/class/power_supply/ | grep -qi BAT; then
  IS_LAPTOP=true
fi

IS_HYPRLAND=false
if echo "$XDG_CURRENT_DESKTOP" | grep -qi "hyprland"; then
  IS_HYPRLAND=true
fi

echo "is laptop: $IS_LAPTOP"
echo "is hyprland: $IS_HYPRLAND"

if [[ "$IS_LAPTOP" == true && "$IS_HYPRLAND" == true ]]; then
  echo "setting up hyprland laptop operation now."
  systemctl --user enable lid-robot.timer
fi
