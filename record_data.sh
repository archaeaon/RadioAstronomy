#!/bin/bash
# NOTE: This script must be run as a non-root user

sudo systemctl stop gpsd.socket
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock

ssd_filepath=/mnt/radio_capstone_ssd

if [ "$1" == "gps" ]
then
	### For setting the system time via GPS ###
	python set_system_time_from_gps.py

elif [ "$1" == "manual" ]
then
	### For setting the system time manually ###
	if [ -z "$1" -o -z "$2" ]
	then
		echo "Error: You must supply the date and time arguments."
		echo "Please provide the desired date and time in the following format."
		echo "Format: arg1=DDMMMYYYY arg2=HH:MM:SS (in 24-hr time format)"
		exit
	elif [[ ! "$1" =~ [0-3][0-9][A-Z][a-z]{2}20[0-9]{2} || ! "$2" =~ [0-2][0-9]:[0-5][0-9]:[0-5][0-9] ]]	# This is technically buggy, but it works for now
	then													# Ex: A dtg of 45Apr2021 31:00:00 is technically allowed
		echo "Error: Date and/or time format unrecognized!"
		echo "Please provide the desired date and time in the following format."
		echo "Format: arg1=DDMMMYYYY arg2=HH:MM:SS (in 24-hr time format)"
		exit
	else
		date --utc +"%d%b%Y %R:%S" --set="$1 $2"	# set the date manually in "DDMMMYYYY HH:MM:SS" format
		date						# print the dtg similar to how the Python script would to show that it worked
	fi

else
	echo "Choose from one of two options:"
	echo "1. gps"
	echo "2. manual"
	exit
fi

gps_date=`date --utc +"%d%b%Y"`

if [ ! -d /mnt/radio_capstone_ssd/"$gps_date" ]	# check if the directory for today's date exists yet
then
	mkdir "$ssd_filepath"/"$gps_date"	# create directory if it doesn't
	#chgrp seds "$ssd_filepath"/"$gps_date"
	#chmod g+w "$ssd_filepath"/"$gps_date"
fi

python3 main.py "$ssd_filepath/$gps_date/"
