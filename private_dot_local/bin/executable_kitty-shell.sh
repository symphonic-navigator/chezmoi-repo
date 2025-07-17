#!/bin/bash

if ! echo "$XDG_CURRENT_DESKTOP" | grep -qi "hyprland"; then
  if command -v zellij >/dev/null 2>&1; then
    exec zellij
  else
    echo "zellij not found, falling back to shell"
  fi
fi

if [ -n "$KITTY_SHELL_OVERRIDE" ]; then
  exec "$KITTY_SHELL_OVERRIDE"
fi

exec "$SHELL"
