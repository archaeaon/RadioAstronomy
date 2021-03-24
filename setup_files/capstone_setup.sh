#!/bin/bash
###### IMPORTANT: Run this script as root from created user!!! ######

echo -e "\nDisabling default user...\n"
bash disable_default_user.sh

echo -e "\nSetting up SSD to automount...\n"
bash ssd_automount_setup.sh

echo -e "\nSetting up GPS...\n"
bash setup_gps.sh

echo -e "\nInstalling LimeSuite...\n"
bash limesuite_install.sh

echo -e "\nUpdating LimeSuite udev-rules...\n"
bash update_limesuite_rules.sh
