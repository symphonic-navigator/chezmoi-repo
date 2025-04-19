#! /bin/bash

set -e

echo "--- chezmoi ---"
cd ~/.local/share/chezmoi
git pull
chezmoi apply

echo "--- updating system via script ---"
cd ~/repos/kde-plasma
git pull
./install.sh

echo "--- updating visor ---"
cd kwin-scripts/visor
./update.sh
