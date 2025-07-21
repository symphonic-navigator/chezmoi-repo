#!/bin/bash

set -e # stop on errors
set -u # fail on unset variables

yay -Syyu

install-pacman() {
  command sudo pacman -S --needed --noconfirm "$@"
}

install-yay() {
  command yay -S --needed --answerclean All --answerdiff N --answeredit N --answerupgrade Y --removemake "$@"
}

# Ask for personal packages
read -p "🔒 Install personal packages (only on your personal kits)? [y/N]: " install_personal
if [[ "$install_personal" =~ ^[Yy]$ ]]; then
  echo "📦 Installing personal packages..."
  install-yay nextcloud-client telegram-desktop
else
  echo "❌ Skipping personal packages."
fi

# Ask for personal packages
read -p "🔒 Install gaming packages? [y/N]: " install_gaming
if [[ "$install_gaming" =~ ^[Yy]$ ]]; then
  echo "📦 Installing gaming packages..."
  install-pacman gamemode steam
  install-yay xpadneo
else
  echo "❌ Skipping gaming packages."
fi

# Ask for extra (toy) packages
read -p "🔒 Install extra (toy) packages? [y/N]: " install_extra
if [[ "$install_extra" =~ ^[Yy]$ ]]; then
  echo "📦 Installing extra (toy) packages..."
  install-pacman cmatrix
  install-yay passpony cowsay rainfall figlet toilet
else
  echo "❌ Skipping extra (toy) packages."
fi

echo "✅ Done! You’re all powered up, captain."
