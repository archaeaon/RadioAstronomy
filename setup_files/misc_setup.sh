#!/bin/bash
###### IMPORTANT: Run this script as a non-root user!!! ######
sudo apt update
sudo apt upgrade
sudo apt install neofetch
pip3 install matplotlib

# This probably isn't needed anymore
#echo -e "\nInstalling pyLMS7002Soapy API...\n"
#wget 'https://github.com/myriadrf/pyLMS7002Soapy/archive/master.zip'
#unzip master.zip
#mv pyLMS7002Soapy-master pyLMS7002Soapy
#python3 pyLMS7002Soapy/setup.py install
#echo -e "\npyLMS7002Soapy API installed\!\n"

# shortcuts for enabling either GUI or terminal boot mode (the Ctrl+Alt+F# method doesn't seem to work too well)
BASH_ALIASES=~/.bash_aliases
touch "$BASH_ALIASES"
echo "alias set-boot-to-terminal='sudo systemctl set-default multi-user.target'" >> "$BASH_ALIASES"
echo "alias set-boot-to-gui='sudo systemctl set-default graphical.target'" >> "$BASH_ALIASES"
echo "alias mount-temp='sudo mount /dev/sdb1 /mnt/temp'" >> "$BASH_ALIASES"
echo "alias umount-temp='sudo umount /mnt/temp'" >> "$BASH_ALIASES"
source "$BASH_ALIASES"

repo_path=~/Documents/github_repo
mkdir "$repo_path"
git -C "$repo_path" clone 'https://github.com/imaquantuman/RadioAstronomy.git'
