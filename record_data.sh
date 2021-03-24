#!/bin/bash
# NOTE: This script must be run as a non-root user

sudo systemctl stop gpsd.socket
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock

ssd_filepath=/mnt/radio_capstone_ssd
gps_date=`python gps_dtg.py`
gps_date=`date --utc +"%d%b%Y" --date="$gps_date"`
echo "$gps_date"
#gps_date=`date --utc +"%d %b %Y"`

if [ ! -d /mnt/radio_capstone_ssd/"$gps_date" ]	# check if the directory for today's date exists yet
then
	mkdir "$ssd_filepath"/"$gps_date"	# create directory if it doesn't
	#chgrp seds "$ssd_filepath"/"$gps_date"
	#chmod g+w "$ssd_filepath"/"$gps_date"
fi

#gps_time=`python get_gps_dtg.py`
#gps_time=`date --utc +"%T %Z" --date="$gps_time"`	# add %p if you'd like to include AM/PM with the time
#gps_time=`date --utc +"%T %Z"`
#echo "it worked" > "$ssd_filepath"/"$gps_date"/"$gps_time".txt
#chgrp users "$ssd_filepath"/"$gps_date"/"$gps_time".txt
#chmod g+w "$ssd_filepath"/"$gps_date"/"$gps_time".txt

python3 main.py "$ssd_filepath/$gps_date/"
