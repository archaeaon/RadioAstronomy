#!/bin/bash
###### IMPORTANT: Run this script as root! It will not work properly if you don't!!! ######

echo -e "Updating repositories...\n"
apt update
apt upgrade

echo -e "Installing TightVNC server...\n"
apt install tightvncserver

echo -e "Creating alias to run TightVNC server...\n"
touch ~/.bash_aliases
echo "alias start-vnc='tightvncserver -nolisten tcp :1 -geometry 1920x1080'" >> ~/.bash_aliases	# this alias can be used to start VNC after remote login through SSH if all else fails
source ~/.bash_aliases

# the below will always start the TightVNC server on port 1 (5901), the idea being port 0 (5900) would always be used for SSH
filepath=/etc/systemd/system/tightvncserver.service
port_number=1	# you can change the port number to whatever desired
user_name=pi	# change the username as appropriate

echo -e "Creating tightvncserver.service in /etc/systemd/system/...\n"
touch "$filepath"
echo "[Unit]" >> "$filepath"
echo "Description=Remote desktop service (VNC)" >> "$filepath"
echo "After=syslog.target network.target" >> "$filepath"
echo >> "$filepath"
echo "[Service]" >> "$filepath"
echo "Type=forking" >> "$filepath"
echo "User=$user_name" >> "$filepath"	# TODO: Change the username here as necessary
echo "PAMName=login" >> "$filepath"
echo "PIDFile=/home/$user_name/.vnc/%H:$port_number.pid" >> "$filepath"
echo "ExecStartPre=-/usr/bin/tightvncserver -kill :$port_number > /dev/null 2>&1" >> "$filepath"
echo "ExecStart=/usr/bin/tightvncserver -nolisten tcp :$port_number -geometry 1920x1080" >> "$filepath"	# the screen resolution here can be changed as necessary
echo "ExecStop=/usr/bin/tightvncserver -kill :$port_number" >> "$filepath"
echo "WorkingDirectory=~" >> "$filepath"
echo >> "$filepath"
echo "[Install]" >> "$filepath"
echo "WantedBy=multi-user.target" >> "$filepath"

# change cursor type from being that annoying "X" shape
filepath=/home/"$user_name"/.vnc/xstartup
echo -e "Altering mouse cursor settings in $filepath...\n"
sed -i "s;xsetroot -solid grey;xsetroot -solid grey -cursor_name left_ptr;" "$filepath"	# replaces the line inside the file at $filepath without needing to use text editor
echo -e "NOTICE: Altering the mouse cursor settings may not have worked. You may need to change it yourself in $filepath..."

echo -e "Reloading daemon...\n"
systemctl daemon-reload
echo -e "Enabling TightVNC server to start on boot...\n"
systemctl enable tightvncserver.service	# the TightVNC server should now be started on boot automatically

echo "The Tight VNC server should now be up and running. You can"
echo "either run 'start-vnc' if you wish to test it immediately"
echo "or you can reboot your machine to test if the server starts"
echo "on boot."
echo "REMINDER: Use port $port_number!"
