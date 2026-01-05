#!/bin/bash

# MultiBrowser setup script for chezmoi

echo "🚀 Setting up MultiBrowser..."

# Create virtual environment
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install PyQt6 PyQt6-WebEngine

# Make scripts executable
chmod +x start_multibrowser.sh

echo "🎉 MultiBrowser setup complete!"
echo ""
echo "Usage:"
echo "  ./start_multibrowser.sh        # Launch with default settings"
echo "  ./start_multibrowser.sh --help # Show all options"

