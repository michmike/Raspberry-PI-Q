#!/usr/bin/python

#================================================================#
# Implemented by Michael Michael http://www.github.com/michmike
# Under MIT License
# https://raw.githubusercontent.com/michmike/Raspberry-PI-Q/master/LICENSE
#================================================================#

import os
import time
from time import sleep
import datetime

sleep(180) # start by sleeping for 3 mins to allow for wifi/internet connectivity

os.chdir("/home/pi/Raspberry-PI-Q")
os.system("sudo git pull")
os.system("sudo cp /home/pi/Raspberry-PI-Q/*.php /var/www/html/.")
os.system("sudo python3 email_IP_address.py")
