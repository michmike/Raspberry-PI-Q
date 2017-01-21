import os

os.chdir("/home/pi/Raspberry-PI-Q")
os.system("sudo git pull")
os.system("sudo python3 email_IP_address.py")