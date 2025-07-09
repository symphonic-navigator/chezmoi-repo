#!/bin/bash

file="$1"
abs_path="$(realpath "$file")"
is_managed=$(chezmoi managed "$abs_path")

if [[ -n "$is_managed" ]]; then
  echo "🧠 Chezmoi edit: $abs_path"
  chezmoi edit "$abs_path"
  chezmoi apply "$abs_path"
else
  echo "✍️  Nvim edit (not managed): $abs_path"
  nvim "$abs_path"
fi
