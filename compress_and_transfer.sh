#!/bin/bash
# $1 should be the date data was recorded

if [ -z "$1" ]
	then
	echo "Please supply the date the data was collected in DDMMMYYYY format."
	echo "Example: compress_and_transfer.sh 01Jan1970"
	
	else
	src_dir=/mnt/radio_capstone_ssd/"$1"
	#dest_dir=/mnt/temp/"$1"
	
	tar -czf "$src_dir"/"$1"_chanA.tar.gz "$src_dir"/*chanA.npy
	tar -czf "$src_dir"/"$1"_chanB.tar.gz "$src_dir"/*chanB.npy
	#mkdir "$dest_dir"
	#cp *chan?.tar.gz "$dest_dir"
fi
