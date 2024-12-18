#!/bin/sh

cd "$(dirname "$0")"

if [ "$(id -u)" != "0" ]; then
  pkexec --keep-cwd env WAYLAND_DISPLAY="$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY" XDG_RUNTIME_DIR=/run/user/0 BUFF_USER="$USER" BUFF_UID="$UID" ./install_essentials.sh
  exit
fi


python3 install_pamac.py
python3 install_telegram.py
python3 install_recording_software.py