#!/usr/bin/env bash

sudo cp ~/.xkb/symbols/de_at_enhanced /usr/share/X11/xkb/symbols/
sudo cp ~/.xkb/symbols/en_us_bastard /usr/share/X11/xkb/symbols/

# add-to-xkb.sh
if ! grep -q "de_at_enhanced" /usr/share/X11/xkb/rules/evdev.lst; then
  echo "🛠  Adding de_at_enhanced to evdev.lst"
  echo "de_at_enhanced    Austrian (Enhanced, AltGr fixes)" | sudo tee -a /usr/share/X11/xkb/rules/evdev.lst
fi

if ! grep -q "<name>de_at_enhanced</name>" /usr/share/X11/xkb/rules/evdev.xml; then
  echo "🛠  Adding de_at_enhanced to evdev.xml"
  sudo sed -i '/<layoutList>/a \
  <layout>\n\
    <configItem>\n\
      <name>de_at_enhanced</name>\n\
      <shortDescription>de+</shortDescription>\n\
      <description>Austrian (Enhanced, AltGr fixes)</description>\n\
      <languageList><iso639Id>de</iso639Id></languageList>\n\
    </configItem>\n\
    <variantList/>\n\
  </layout>' /usr/share/X11/xkb/rules/evdev.xml
fi
