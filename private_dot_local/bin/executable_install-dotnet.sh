#! /bin/bash

sudo pacman -Syyu --noconfirm

sudo pacman -Syyu --needed --noconfirm \
  dotnet-sdk-8.0 \
  dotnet-sdk-9.0

# install dotnet scripting
dotnet tool install -g dotnet-script
