#! /bin/bash

cd ~/.local/share/chezmoi
git pull
chezmoi apply

cd ~/repos/kde-plasma
git pull
./install.sh

