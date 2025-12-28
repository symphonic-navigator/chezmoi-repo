#!/usr/bin/env bash

ROFI_PID=$(pgrep -x rofi)

# Check if rofi is running and what mode
if [ -n "$ROFI_PID" ]; then
  ROFI_CMD=$(ps -p "$ROFI_PID" -o args --no-headers)

  if echo "$ROFI_CMD" | grep -q "show drun"; then
    # Same mode - just close it
    pkill rofi
    exit 0
  else
    # Different mode - kill and restart with new mode
    pkill rofi
    sleep 0.1
  fi
fi

# Start rofi in drun mode
rofi -show drun -modi drun,window
