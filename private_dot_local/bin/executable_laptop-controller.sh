#!/bin/bash

INTERNAL_SCREEN='eDP-1'
SCREEN_ON=', preferred, auto, 1'
SCREEN_OFF=', disable'
KBD_BACKLIGHT_DEVICE='white:kbd_backlight'
LID_OPEN_KEYBOARD_BACKLIGHT_BRIGHTNESS=1

# Get all connected monitor names
CONNECTED=$(hyprctl monitors all | grep -E '^Monitor' | awk '{print $2}')

# Assume internal is needed unless we find an external
EXTERNAL_CONNECTED=0

for MON in $CONNECTED; do
  if [[ "$MON" != "$INTERNAL_SCREEN" ]]; then
    EXTERNAL_CONNECTED=1
    hyprctl keyword monitor "$MON $SCREEN_ON"
  fi
done

if [[ "$EXTERNAL_CONNECTED" -eq 1 ]]; then
  # External monitor present: disable internal display
  brightnessctl --quiet --device=$KBD_BACKLIGHT_DEVICE set 0
  hyprctl keyword monitor "$INTERNAL_SCREEN $SCREEN_OFF"
else
  # No external monitor: enable internal display
  LID_STATE=$(cat /proc/acpi/button/lid/LID*/state)

  if [[ "$LID_STATE" == *closed* ]]; then
    KBD_BACKLIGHT_BRIGHTNESS="$LID_OPEN_KEYBOARD_BACKLIGHT_BRIGHTNESS"
  else
    KBD_BACKLIGHT_BRIGHTNESS=0
  fi

  brightnessctl --quiet --device=$KBD_BACKLIGHT_DEVICE set "$KBD_BACKLIGHT_BRIGHTNESS"
  hyprctl keyword monitor "$INTERNAL_SCREEN $SCREEN_ON"
fi
