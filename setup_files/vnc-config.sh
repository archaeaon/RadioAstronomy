#!/bin/bash
# IMPORTANT: Run this file as the non-root user!!!

port_number=1
#tightvncserver -kill :"$port_number"
tightvncserver -nolisten tcp :"$port_number" -geometry 1920x1080

filepath=~/.vnc/xstartup

# change cursor type from being that annoying "X" shape
echo -e "Altering mouse cursor settings in $filepath...\n"
sed -i "s;xsetroot -solid grey;xsetroot -solid grey -cursor_name left_ptr;" "$filepath"	# replaces the line inside the file at $filepath without needing to use text editor
echo -e "NOTICE: Altering the mouse cursor settings may not have worked. You may need to change it yourself in $filepath..."
