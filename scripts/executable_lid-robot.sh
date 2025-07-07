#! /bin/bash

LID_STATE=$(cat /proc/acpi/button/lid/LID*/state)

KBD_BACKLIGHT_DEVICE='white:kbd_backlight'

INTERNAL_SCREEN='eDP-1'
SCREEN_ON=', preferred, auto, 1'
SCREEN_OFF=', disable'

if [[ "$LID_STATE" == *closed* ]]; then
  brightnessctl --quiet --device=$KBD_BACKLIGHT_DEVICE set 0
  hyprctl --quiet keyword "monitor $INTERNAL_SCREEN $SCREEN_OFF"
else
  brightnessctl --quiet --device=$KBD_BACKLIGHT_DEVICE set 1
  hyprctl --quiet keyword "monitor $INTERNAL_SCREEN $SCREEN_ON"
fi
