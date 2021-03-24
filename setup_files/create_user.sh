#!/bin/bash
###### NOTE: Run this script as root from the default user!!! ######

username=seds
default_username=pi

adduser "$username"

for group in `groups "$default_username"`
do
	if [ "$group" == "$default_username" -o "$group" == ":" ]
	then
		continue
	fi
	
	adduser "$username" "$group"
done

groups "$username"

echo "The user $username has been created."
echo "You should now logout of default user $default_username and disable or remove it."
