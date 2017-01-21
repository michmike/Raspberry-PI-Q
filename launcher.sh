#!/bin/sh
# launcher.sh
# requires crontab; Install using: sudo apt-get install gnome-schedule
# Create crontab using: @reboot sh /home/pi/raspberry-pi-q/launcher.sh
# Check scheduled tasks using: crontab -l

cd /
cd home/pi/Raspberry-PI-Q 
sudo git pull
sudo python3 email_IP_address.py
#sudo git clone https://github.com/michmike/Raspberry-PI-Q.git  
cd /