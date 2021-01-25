#!/bin/bash
###### IMPORTANT: Run this script as root! It will not work properly if you don't!!! ######

#echo -e "Creating alias to run TightVNC server...\n"
#touch ~/.bash_aliases
#echo "alias start-vnc='tightvncserver -nolisten tcp :1 -geometry 1920x1080'" >> ~/.bash_aliases	# this alias can be used to start VNC after remote login through SSH if all else fails
#source ~/.bash_aliases

# the below will always start the TightVNC server on port 1 (5901), the idea being port 0 (5900) would always be used for SSH
filepath_service=/etc/systemd/system/radio_astronomy.service
user_name=pi	# TODO: Change the username here as necessary
filepath_script=/home/"$user_name"/<put rest of filepath here>/receive.py	# TODO: Fill in the rest of the filepath to the Python script

echo -e "Creating radio_astronomy.service in /etc/systemd/system/...\n"
touch "$filepath_service"
echo "[Unit]" >> "$filepath_service"
echo "Description=Radio astronomy data collection script" >> "$filepath_service"
echo "After=syslog.target network.target" >> "$filepath_service"
echo >> "$filepath_service"
echo "[Service]" >> "$filepath_service"
echo "Type=forking" >> "$filepath_service"
echo "User=$user_name" >> "$filepath_service"
echo "PAMName=login" >> "$filepath_service"
echo "PIDFile=$filepath_script" >> "$filepath_service"	# TODO: Make sure this will work as intended or if this field is even necessary
#echo "ExecStartPre=-/usr/bin/tightvncserver -kill :$port_number > /dev/null 2>&1" >> "$filepath_service"	# TODO: LimeSDR might need to be activated here before calling Python script (precautionary)
echo "ExecStart=/usr/bin/python3 $filepath_script" >> "$filepath_service"
#echo "ExecStop=/usr/bin/tightvncserver -kill :$port_number" >> "$filepath_service"
echo "WorkingDirectory=~" >> "$filepath_service"	# TODO: Change working directory as needed
echo >> "$filepath_service"
echo "[Install]" >> "$filepath_service"
echo "WantedBy=multi-user.target" >> "$filepath_service"

echo -e "Reloading daemon...\n"
systemctl daemon-reload
echo -e "Enabling the radio astronomy Python script to start on boot...\n"
systemctl enable radio_astronomy.service	# the Python script should now be started on boot automatically

echo "The radio astronomy data collection script should now start"
echo "on boot. Reboot your machine to test if the script starts"
echo "as intended."
