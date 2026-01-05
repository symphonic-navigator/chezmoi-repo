#!/bin/bash

# MultiBrowser startup script
# Activates virtual environment and launches the application

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Activate the virtual environment
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
  source "$SCRIPT_DIR/venv/bin/activate"
  echo "Virtual environment activated"
else
  echo "Virtual environment not found. Please run: python3 -m venv venv"
  exit 1
fi

# Check if required packages are installed
if ! python3 -c "import PyQt6.QtWebEngineWidgets" 2>/dev/null; then
  echo "Required packages not found. Installing..."
  pip install PyQt6 PyQt6-WebEngine
fi

# Launch the application with default window class for Hyprland
python3 "$SCRIPT_DIR/main.py" --window-class "tk-scratchpad" "$@"

deactivate

