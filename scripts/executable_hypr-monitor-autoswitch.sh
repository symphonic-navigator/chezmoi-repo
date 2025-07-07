#!/bin/bash

# Your internal display name
INTERNAL="eDP-1"

# Loop forever
while true; do
  # Get all connected displays
  connected=()
  for statusfile in /sys/class/drm/*/status; do
    if grep -q "connected" "$statusfile"; then
      name=$(basename "$(dirname "$statusfile")")
      connected+=("$name")
    fi
  done

  # Determine what to do
  external_connected=()
  for name in "${connected[@]}"; do
    if [[ "$name" != *"$INTERNAL"* ]]; then
      external_connected+=("$name")
    fi
  done

  if ((${#external_connected[@]} > 0)); then
    # External display is connected: enable external(s), disable internal
    echo "Detected external monitor(s): ${external_connected[*]}"
    hyprctl keyword monitor "$INTERNAL,disable"
    for ext in "${external_connected[@]}"; do
      hyprctl keyword monitor "$ext,preferred,0x0,1"
    done
  else
    # Only internal is connected
    echo "Only $INTERNAL connected"
    hyprctl keyword monitor "$INTERNAL,preferred,0x0,1"

    # Disable all other monitors just in case
    for mon in "${connected[@]}"; do
      if [[ "$mon" != *"$INTERNAL"* ]]; then
        hyprctl keyword monitor "$mon,disable"
      fi
    done
  fi

  # Sleep before checking again
  sleep 5
done
