#! /bin/bash

set -e

echo "--- chezmoi ---"
cd ~/.local/share/chezmoi
git pull
chezmoi apply
