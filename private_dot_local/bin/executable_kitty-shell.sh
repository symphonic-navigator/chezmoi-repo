#!/bin/bash

if [ -n "$KITTY_SHELL_OVERRIDE" ]; then
  exec "$KITTY_SHELL_OVERRIDE"
fi

exec "$SHELL"
