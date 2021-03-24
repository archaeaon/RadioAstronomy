#sudo btrfs filesystem label /dev/sda1 radio_capstone_ssd
sudo mkdir /mnt/radio_capstone_ssd
sudo echo "LABEL=radio_capstone_ssd /mnt/radio_capstone_ssd btrfs defaults,auto,users,rw,nofail,x-systemd.device-timeout=15 0 0" >> /etc/fstab
sudo chgrp users /mnt/radio_capstone_ssd
sudo chmod g+w /mnt/radio_capstone_ssd