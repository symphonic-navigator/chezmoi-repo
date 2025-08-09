#! /bin/bash

hyprctl --instance 0 'keyword misc:allow_session_lock_restore 1'
killall -9 hyprlock
hyprctl --instance 0 'dispatch exec hyprlock'

echo "press alt+ctrl+f2 to login in now"
