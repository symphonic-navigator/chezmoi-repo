#!/bin/bash

INTERNAL_SCREEN='eDP-1'
SCREEN_ON=', preferred, auto, 1'
SCREEN_OFF=', disable'
KBD_BACKLIGHT_DEVICE='white:kbd_backlight'

# Get all connected monitor names
CONNECTED=$(hyprctl monitors all | grep -E '^Monitor' | awk '{print $2}')

# Assume internal is needed unless we find an external
EXTERNAL_CONNECTED=0

for MON in $CONNECTED; do
  if [[ "$MON" != "$INTERNAL_SCREEN" ]]; then
    EXTERNAL_CONNECTED=1
    break
  fi
done

if [[ "$EXTERNAL_CONNECTED" -eq 1 ]]; then
  # External monitor present: disable internal display
  brightnessctl --quiet --device=$KBD_BACKLIGHT_DEVICE set 0
  hyprctl keyword monitor "$INTERNAL_SCREEN $SCREEN_OFF"
else
  # No external monitor: enable internal display
  brightnessctl --quiet --device=$KBD_BACKLIGHT_DEVICE set 1
  hyprctl keyword monitor "$INTERNAL_SCREEN $SCREEN_ON"
fi
