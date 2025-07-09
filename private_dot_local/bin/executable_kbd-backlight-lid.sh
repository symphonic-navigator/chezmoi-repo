#!/bin/bash

DEVICE='white:kbd_backlight'
LID_STATE=$(cat /proc/acpi/button/lid/LID*/state)

if [[ "$LID_STATE" == *closed* ]]; then
  brightnessctl --device=$DEVICE set 0
else
  brightnessctl --device=$DEVICE set 1
fi
