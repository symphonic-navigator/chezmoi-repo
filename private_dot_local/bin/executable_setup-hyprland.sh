#! /bin/bash

set -e
set -u

GPU_ENV_FILE=$HOME/.config/hypr/UserConfigs/gpu_env.local.conf

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

# --- Hardware Setup ---

if inxi -G | grep -iq nvidia; then
  IS_NVIDIA=true
else
  IS_NVIDIA=false
fi

if [[ "$IS_NVIDIA" == true ]]; then
  echo "ℹ️ nvidia detected!"
  cp ~/.config/hypr/UserConfigs/hardware/nvidia_env.conf "$GPU_ENV_FILE"

  echo "🔧 Enabling nvidia power management..."
  sudo systemctl enable --now nvidia-powerd.service
else
  echo "ℹ️ non-nvidia GPU detected!"
  cp ~/.config/hypr/UserConfigs/hardware/other_gpu_env.conf "$GPU_ENV_FILE"
fi

# --- Common Setup ---
systemctl --user enable --now hyprland-keep-kitty-quake-alive.timer
systemctl --user enable --now hyprland-keep-ncspot-alive.timer
echo "✅ common hyprland setup."

if [[ "$IS_LAPTOP" == false ]]; then
  echo "ℹ️ not a laptop, exiting."
  exit 2
fi

# --- Laptop Setup ---
echo "✅ hyprland laptop setup successfully established."

# --- Reload hyprland ---
hyprctl reload -q
echo "✅ hyprctl reload successfully performed."
