sudo apt update
sudo apt upgrade
sudo apt install -y limesuite liblimesuite-dev soapysdr-module-lms7

wget 'https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh'
bash Anaconda3-2020.07-Linux-x86_64.sh	# installing anaconda provides all the data science-related packages we'll need, including numba
conda update conda						# update anaconda environment
conda update anaconda
conda install -c conda-forge soapysdr	# soapysdr will just need to be installed through anaconda for it to work

rm Anaconda3-2020.07-Linux-x86_64.sh	# remove the anaconda installer since we won't need it anymore
