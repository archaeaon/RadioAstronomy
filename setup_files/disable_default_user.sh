#!/bin/bash
###### NOTE: Run this script as root from the created user!!! ######

default_username=pi
username=seds

echo "Making default user $default_username inactive..."
pkill -u "$default_username"
echo "Disabling account for default user $default_username..."
usermod --expiredate 1 "$default_username"

echo "Default user $default_username has been disabled."

echo "setting auto-login to user $username..."
sed -i "s;autologin-user=$default_username;autologin-user=$username;" /etc/lightdm/lightdm.conf
