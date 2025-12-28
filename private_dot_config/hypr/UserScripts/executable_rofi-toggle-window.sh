#!/usr/bin/env bash

ROFI_PID=$(pgrep -x rofi)
CURRENT_MODE=""

# Check if rofi is running and what mode
if [ -n "$ROFI_PID" ]; then
  # Get rofi command line to determine mode
  ROFI_CMD=$(ps -p "$ROFI_PID" -o args --no-headers)

  if echo "$ROFI_CMD" | grep -q "show window"; then
    # Same mode - just close it
    pkill rofi
    exit 0
  else
    # Different mode - kill and restart with new mode
    pkill rofi
    sleep 0.1
  fi
fi

# Start rofi in window mode
rofi -show window -modi drun,window
