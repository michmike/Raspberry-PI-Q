import os

os.chdir("/home/pi/Raspberry-PI-Q")
os.system("sudo git pull")
os.system("sudo cp /home/pi/Raspberry-PI-Q/index.html /var/www/html/.")
os.system("sudo python3 email_IP_address.py")
