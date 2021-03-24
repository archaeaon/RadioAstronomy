#!/bin/bash
###### IMPORTANT: Run this script as root! It will not work properly if you don't!!! ######

echo -e "Updating repositories...\n"
apt update
apt upgrade

echo -e "Installing TightVNC server...\n"
apt install tightvncserver

user_name=seds	# change the username as appropriate
port_number=1	# you can change the port number to whatever desired
BASH_ALIASES=/home/"$user_name"/.bash_aliases

echo -e "Creating alias to run TightVNC server...\n"
touch "$BASH_ALIASES"
echo "alias start-vnc='tightvncserver -nolisten tcp :$port_number -geometry 1920x1080'" >> "$BASH_ALIASES"	# this alias can be used to start VNC after remote login through SSH if all else fails
echo "alias stop-vnc='tightvncserver -kill :$port_number'" >> "$BASH_ALIASES"	# this can be used to stop tightvncserver

# the below will always start the TightVNC server on port 1 (5901), the idea being port 0 (5900) would always be used for SSH
filepath=/etc/systemd/system/tightvncserver.service

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

echo -e "Reloading daemon...\n"
systemctl daemon-reload
echo -e "Enabling TightVNC server to start on boot...\n"
systemctl enable tightvncserver.service	# the TightVNC server should now be started on boot automatically

echo "The Tight VNC server should now be up and running."
echo "IMPORTANT: Run 'start-vnc' before running vnc-config.sh!"
echo "           You may need to source $BASH_ALIASES first."
