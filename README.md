# Raspberry-PI-Q
Heavily influenced by [@justindean](https://github.com/justindean) and his [PitmasterPI](https://github.com/justindean/PitmasterPi) project, I decided to create an advanced BBQ temperature controller using a Raspberry PI (RPI) for kamado style grills (like the Big Green Egg and Kamado Joe). The goals of the project were the following:
* Make delicious and consistently great BBQ
* Use RPI to control the fan and the air intake of the grill. This means you control the temperature of the charcoal
* Use RPI and predictive algorithms to let me know the exact time when my meat will reach the desired temperature
* Get frequent notifications on how the cookout is going
* Use RPI and email/text notifications if my desired intent is not met
* Make it affordable
* Create cool dashboards to show off my cooking

The biggest difference of this project from the one @justindean created is the fact that i wanted to be able to have two thermocouples so that i can also monitor the temperature of the meat. That meant I had to write pretty much all of the code from scratch. Using simple growth rate math, I can use all these data to predict when my BBQ would reach the desired temperature. The updated BOM is listed below.

Before you get started on using Raspberry-PI-Q, make sure you read and understand the terms of the [MIT license](https://github.com/michmike/Raspberry-PI-Q/blob/master/LICENSE) attached to this project.

## Bill of Materials (BOM)
| Functionality | Item | Price | Link |
| ------------- | ---- | ----- | ---- |
| Computer | Raspberry Pi 3 Model B Motherboard | $41 | https://www.amazon.com/Raspberry-Pi-RASP-PI-3-Model-Motherboard/dp/B01CD5VC92 |
| Power Supply | 5V 2.5A power supply  | $10 | https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Charger/dp/B00MARDJZ4 |
| Memory | Samsung 16GB microSDHC Class 10 | $10 | https://www.amazon.com/Samsung-Adapter-MB-MP16DA-Packaging-Extender/dp/B01527LASQ |
| Fan | DC 12V Squirrel Cage brushless fan (up to 0.5amps ~ 6 watts) | $10 | https://www.amazon.com/gp/product/B00B2ARV22 |
| Fan Power | 3v-12v DC 1amp/12watts adjustable power supply for the fan | $11 | https://www.amazon.com/gp/product/B015PXUHYA |
| Thermocouple #1 | uxcell K Type 0-400C Thermocouple 5cm Probe, 1M length | $5 | https://www.amazon.com/gp/product/B00899A4LY |
| Thermocouple #2 | uxcell K Type 0-800C Thermocouple 10cm Probe, 2M length | $5 | https://www.amazon.com/gp/product/B00C97J0LC |
| Thermocouple Plate | Robogaia Dual Thermocouple Plate for Raspberry | $50 | http://www.robogaia.com/raspberry-pi-dual-thermocouple-plate.html |
| Relay | JBtek 4-channel DC 5V Relay Module AC250V/10A, DC30V/10A | $7 | https://www.amazon.com/gp/product/B00KTEN3TM |
| Wiring | Sunkee Female to Female 1P-1P 20cm jumper cables, 100 pcs | $8 | https://www.amazon.com/gp/product/B00AYCON8Y |
| Case | Case to house and protect all the equipment | TBD | TBD |

## Competition
If you are looking for non-DIY alternatives, the products from [BBQ Guru](http://www.bbqguru.com/) seem to fit the bill
* CyberQ offers almost identical functionality for $329
* DigiQ offers smoker and meat temperature control without any alerting/notifications or internet access for $219
* PartyQ only offers smoker temperature control for $150

## Wiring Instructions
* Look at the PIN numbers of the RPI on the pictures listed below before you get started. Also look at some of my detailed pictures and follow the color coding of the wires
* Connect the Robogaia dual thermocouple plate
  * The plate fits flush on top of the RPI on one end of the RPI extensibility connectors. Look at the pictures below as well as the documentation at http://www.robogaia.com/raspberry-pi-dual-thermocouple-plate.html for more details
* Connect the relay to the Robogaia plate and the RPI
  * Useful post: https://www.amazon.com/gp/customer-reviews/RUNBAXRMMUMBL/ref=cm_cr_arp_d_rvw_ttl?ie=UTF8&ASIN=B00KTEN3TM
  * Useful video: https://www.youtube.com/watch?v=OQyntQLazMU
  * There are two rows of input pins (GND IN1 IN2 IN3 IN4 VCC) on the relay board and (JD-VCC VCC) with the latter coming with a jumper bridging the pins
    * Keep the jumper for (JD-VCC VCC) on
    * [Blue Wire] Connect a wire from GND on your RPI (pin #6) to GND on the relay module
    * [Red Wire] Connect a wire from the 5V pin on your RPI (pin #2) to the VCC pin that is adjacent to IN4 (not the one next to JD-VCC!) on the relay
    * [Yellow Wire] Finally hook the GPIO 26 (pin #37) of the RPI to IN2 of the relay
    * Set the pin to 'low' or 0V in the software to activate and 'high' or 3.3V-5V to deactivate
  * Run `sudo python3 relay_tester.py` from the source code below to test the relay on/off operations
* Splice the power source for the 12v DC power source for the fan and have it go through the relay IN2 so that the relay can control the on/off power supply for the fan
* Connect the two K thermocouples to the correct +/- on the Robogaia plate
  * Look at the wiring pictures below that have labelled which is the Meat and which is the Grill thermocouple
* Connect the power supply to the RPI. Micro-USB power supply has to be at least 2 amps
 
## Setting up the Raspberry PI 3 Model B
You only need to perform the following steps once!
* Download NOOBS zip file from https://www.raspberrypi.org/downloads/
* Format your microSD card to FAT32 as per https://www.raspberrypi.org/documentation/installation/sdxc_formatting.md
* Extract zip files using 7zip to the SD card as per https://www.raspberrypi.org/learning/software-guide/quickstart/
* Connect all the RPI components (mouse, keyboard, network, HDMI, etc)
* Put the microSD into the RPI and connect the power to start it up. Make sure the power source is at least 2 amps.
  * Pick Raspian (the full operating system) and select Install
  * Follow the instructions to set up the RPI on first boot and eventually it will boot to the graphical user interface
* Update to the latest software as per https://www.raspberrypi.org/learning/software-guide/update-sd-card/
  * `sudo apt-get update`
  * `sudo apt-get upgrade`
* You should change your default password (i.e. raspberry) as per https://www.raspberrypi.org/documentation/linux/usage/users.md
  * `passwd`
* SSH into the RPI as per https://www.raspberrypi.org/documentation/remote-access/ssh/unix.md and https://www.raspberrypi.org/documentation/remote-access/ssh/
  * `sudo raspi-config`
  * Pick Advanced options>ssh>Enable
  * `sudo reboot`
  * `hostname -I` [to get the IP address]
  * You can now SSH into the RPI using username `pi@192.168.1.5` or simply `pi` and the password you set above
* Configure networking and DNS servers if necessary
  * `sudo pico /etc/network/interfaces` [update the file with the following lines, substituting 192.168.1.254 for your DNS server]
    * `auto eth0`
    * `iface eth0 inet dhcp`
    * `[4spaces]dns-search google.com`
    * `[4spaces]dns-nameservers 192.168.1.254`
  * Might need to do the same config for wlan0, the wifi interface
    * `iface wlan0 inet dhcp`
  * `sudo /etc/init.d/networking restart`
  * `cat /etc/resolv.conf` [verify nameserver is set]
  * `sudo route -n` [verify routes are set]
  * `ip route show` [verify routes are set]
* Use the instructions to enable i2c needed by the thermocouple plate as per http://www.robogaia.com/raspberry-pi-dual-thermocouple-plate.html
  * `sudo apt-get install python-smbus`
  * `sudo apt-get install i2c-tools`
  * `sudo nano /etc/modules` [opens a file]
    * Add  to the end of the file /etc/modules these lines (if those are not present already)
      * `i2c-dev`
      * `i2c-bcm2708`
  * `sudo nano /etc/modprobe.d/raspi-blacklist.conf`
    * Change:
      * `blacklist spi-bcm2708`
      * `blacklist i2c-bcm2708`
    * To:
      * `#blacklist spi-bcm2708`
      * `#blacklist i2c-bcm2708`
  * Make sure i2c is enabled for the RPI. You can enable it using the commands below or alternatively enable it using the GUI and the advanced options of `sudo raspi-config` as per https://www.raspberrypi.org/documentation/configuration/raspi-config.md
    * `sudo nano /boot/config.txt` and uncomment the line below
      * `dtparam=i2c_arm=on`
    * `sudo reboot`
    * `sudo i2cdetect -y 1` to verify if i2c is enabled
  * Run `sudo python3 dual_read_temperature_fahrenheit.py` from the source code below to test the thermocouples
* Install dweepy, a library needed by Dweet.io
  * `sudo python3 -m pip install dweepy`
* Use crontab to create a reboot/startup task
  * `crontab -e` [will open up a file. use nano as the editor, and insert the following line]	
    * `@reboot sudo python3 /home/pi/Raspberry-PI-Q/launcher.py &`
  * `crontab -l` [to see the changes]
  * `service cron status` [to see active jobs]
* Install git and pull down the repo for this project
  * `sudo apt-get install git`
  * `cd /home/pi`
  * `sudo git clone https://github.com/michmike/Raspberry-PI-Q.git`
  * `sudo git status` [get status of files locally]
  * `sudo git reset --hard` [reverts any local changes - *Use Carefully*]
* Enable wifi using graphical interface as per https://www.raspberrypi.org/learning/software-guide/wifi/ or using the command line as per https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
  * `sudo iwlist wlan0 scan | grep ESSID`
  * `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
  * Enter the following details on the file
 ```
 network={  
     ssid="[wifi access point name, ESSID]"  
     psk="[wifi password]"  
 }  
 ```
  * `sudo ifdown wlan0` [optional]
  * `sudo ifup wlan0` [optional]
  * `sudo reboot`
  * `ifconfig wlan0` [verify you were able to get an IP Address for the wifi connection]
* If you want to change the timezone to be other than GMT/UTC. Currently the RPI gets its time from an internet time server
  * `sudo dpkg-reconfigure tzdata`
* Create a webserver and enable PHP
  * `sudo apt-get install apache2 php5 libapache2-mod-php5`
  * `sudo service apache2 restart`
  * `cd /var/www/html`
  * `sudo cp /home/pi/Raspberry-PI-Q/index.php /var/www/html/.`
  * Make sure  that the Apache user (www-data) has access to execute sudo commands
    * `sudo nano /etc/sudoers`
    * Add the following line `www-data ALL=(ALL) NOPASSWD: ALL`
  * Visit your site at `http://<RPI IP Address>/index.php` and read all the documentation
  * After you execute a command on the website, you can check if the python process started using
    * `ps -u www-data`
    * `ps aux  | grep python3`

## Development Instructions
* Install Python for Windows
* Install Visual Studio Code with the python extension from https://marketplace.visualstudio.com/items?itemName=donjayamanne.python
* Install PIP as per instructions from https://pip.pypa.io/en/stable/installing/
* Create an account with www.dweet.io and www.freeboard.io. You don't need to pay for a locked object. You can create your own board and save it with your own dashboard analytics for this project
  * Use the two files below to enhance and create your own html-based dashboards on freeboard
* Create an account with www.gmx.com to get a free email address
* Create an account with www.grovestreams.com. 
  * Create an organization and under advanced enable the "Raspberry PI Metrics" blueprint
  * For more details, read https://www.grovestreams.com/developers/getting_started_rpi.html
  * Once your account is created, go to the Dashboard and click on Admin>API Keys>Click on Feed Put API Key>View Secret Key. You need to save this key as this is needed as input to the Raspberry-PI-Q. See below for more details.
  * For your streams\components, create at least two notifications via email (free). When you create the notification, make sure to select an "Action Package" 
		 * A value condition event notification so that you are notified if your meat or grill falls out of any specific ranges
		 * A latency event so that you are notified immediately if data is not coming from the RPI, which means something went wrong. This is a very simplistic type of outside-in monitoring

## Source Code
| File | Description |
| ------------- | ---- |
| Raspberry-PI-Q.py | Contains all the logic of the temperature controller. See below for details on its input parameters |
| index.php | PHP webpage to control the startup and teardown of the Raspberry-PI-Q python program. It also includes test utilities and real time logging output from the RPI |
| processID.php | Simple PHP webpage to check if the process ID from the URL is still running on the RPI |
| monitor.php | Simple PHP webpage to check if the process ID from the URL is still running on the RPI and also to display the real time output from Dweet on the progress of your grilling. You can invoke this page as `http://<IP Address>/monitor.php?PID=14903` where 14903 is the process ID for the execution of Raspberry-PI-Q |
| launcher.py | This is the python script executed at reboot of the RPI and it refreshes the code from the github repo as well as call the email address program below. It also copies the updated PHP website to the right location |
| email_IP_address.py | This is a python program that will email and use dweet.io to update the current IP address of the RPI |
| Freeboard_HTML_MeatChart.txt | This is the sample freeboard.io HTML section for advice on best cooking temperatures. Copy the file contents and create an html-based dashboard on freeboard.io |
| Freeboard_HTML_Dashboard.txt | This is the sample freeboard.io HTML section for the custom temperature dashboard. Copy the file contents and create an html-based dashboard on freeboard.io | 
| relay_tester.py | This is a python program to test the relay by turning it on and off every few seconds |
| dual_read_temperature_fahrenheit.py | This is a python program to test the dual thermocouple plate by capturing and printing the current temperature of each thermocouple every few seconds |

## Startup Operations
**__Perform these steps every time you grill!__**
* Light up a couple of charcoal brickets in your grill
* Attach the fan plate to your input air vent as per pictures
* Open the output vent on top of your egg slightly as per pictures
* Power up the RPI and attach the power source for the fan
* SSH using putty.exe (https://the.earth.li/~sgtatham/putty/latest/x86/putty.exe to download)
  * Enter the IP address for your RPI as outlined below in the __Host Name__ field and then select __SSH__ and click __Open__
  * IP address: 192.168.1.13. Find it using https://dweet.io/follow/Raspberry-PI-Q-IPAddress 3-4 minutes after your device starts
  * A terminal window will now open
  * Username: pi
  * Password: [whatever you set in the instructions to update the password above]
* Once you login you will get access to the RPI's operating system
* `cd /home/pi/Raspberry-PI-Q/`
* Run the command to start the Raspberry-PI-Q. Alternatively you can visit `http://192.168.1.14/index.php` to operate the Raspberry-PI-Q from the graphical interface. Replace the IP Address with your own from the step above
  * `sudo python3 Raspberry-PI-Q.py 180 225 125 email@address.com 5 30 Raspberry-PI-Q-Michael ff83612c-6814-466e-bd51-5d55039c184e &`
  * _All temperatures are in fahrenheit_
  * 1st parameter: 180 is the setup temperature of the grill. The fan will run continuously until this temperature is reached
  * 2nd parameter: 225 is the desired temperature of the grill. The program will turn on/off the fan to maintain this temperature
  * 3rd parameter: 125 is the desired temperature of the meat. Insert the probe in the meat and we will predict the time when it will be ready
  * 4th parameter: This is the email address for notifications. You can alternatively use 10digitphonenumber@txt.att.net or 10digitphonenumber@tmomail.net for email-to-text
  * 5th parameter: This is the interval in minutes you want to receive regular updates and notifications. Alerts will come immediately
  * 6th parameter: This is the interval in seconds that each loop will take. if set to 30 seconds, assume the fan will run X seconds every 30 seconds. You can adjust this for more or less fan time during your interval
  * 7th parameter: This is the unique name for your device that you want to use for tracking analytics on Dweet, Freeboard, and Grovestreams
    * i.e. Raspberry-PI-Q-Michael
  * 8th parameter: This is the unique application API ID you get from your grovestreams account as per instructions above
    * i.e. ff83612c-6814-466e-bd51-5d55039c184e
* Press `ctrl-c` to exit the program and terminate the monitoring by Raspberry-PI-Q
* Adjust the voltage to the fan according to weather conditions and size of grill. 4-6 volts should work great
* Visit https://dweet.io/follow/Raspberry-PI-Q-Michael [Change the URL to match your 7th parameter] for the raw data
* Visit freeboard.io/board/[your board id that you created earlier] for the dashboard
* Visit https://www.grovestreams.com, click on your organization, and go to Dashboards to view/create charts and alerts  
* Shutdown the RPI before removing the power cord using `sudo shutdown -h now`

## Future Ideas
Some things I want to explore for a v2 of this project include
* Use most of the same hardware to create a sous vide immersion circulator
* Add a high-heat camera to take pictures of my meat _inside_ the grill
* Adopt the Facebook Messenger Bot architecture to create a bot for my Raspberry-PI-Q
* Change the algorithm to a more traditional PID https://en.wikipedia.org/wiki/PID_controller. There are lots of python libraries for PID

## Pictures
### Click on them to see them bigger in size
1. Relay and Power Wiring for Ground, VCC, and Relay IN2  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_001929.jpg" width="375" height="500">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/relay.JPG" width="800" height="600">          
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/relaysetup.JPG" width="800" height="600">
2. Fan and fan adaptor for kamado style grill's bottom air vent. Use aluminum high-heat tape where necessary  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002004.jpg" width="375" height="500">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/kamadoconnector.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/fanassembly.JPG" width="800" height="600">
3. Robogaia board pass-through connection to 5v power, ground, and GPIO 26  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002514.jpg" width="375" height="500">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/wiringonthermocouple_1.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/wiringonthermocouple_2.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_9539.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_9538.JPG" width="800" height="600">
4. Thermocouples on the robogaia dual board  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002521.jpg" width="375" height="500">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/thermocoupleplate.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/thermocouplesetup.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_9540.JPG" width="800" height="600">
5. PIN layout for Raspberry  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/RaspberryPI2_PIN_layout.jpg">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/RaspberryPI3_PIN_layout.jpg">
6. Example Text/Email Notification  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/emailnotification.png">
7. Example email alert coming from Grovestreams  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/email-alert.png">
8. Inactivity outside-in monitoring alert by Grovestreams  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/outside-in-monitoring.png">
9. Parts  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/parts.jpg">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/thermocouple.JPG" width="800" height="600">
10. Top air vent for kamado grills (top vent - air and smoke goes out from here). Adjust this depending on temperature and air flow you require  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/topvent.jpg" width="800" height="600">
11. Input air vent for kamado grills (bottom vent - air comes in through here)  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/air_intake.JPG" width="800" height="600">
12. Fire box - light up just a single charcoal and get the Raspberry-PI-Q started  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/firebox.JPG" width="800" height="600">
13. My *custom* case for the RPI and all its components (top and side view)  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/customcase1.JPG" width="800" height="600">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/customcase2.JPG" width="800" height="600">
14. Grovestreams dashboard  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/grovestreams.png">
15. Freeboard.IO dashboard  
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/FreeboardDashboard.png">
16. Raspberry-PI-Q website 
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/phpWebsite.png">
17. Cooking pictures with the device attached on the kamado grill. 9lb bone-in pork shoulder dry rubbed with williams-sonoma chili-lime rub smoked at 225F for ~7hrs. At 160F I foiled it with apple sauce up to 200F when it was shredded.
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/marinated.jpg">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/Raspberry-PI-Q.jpg">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/smoking.jpg">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/porkshoulder_complete.jpg">
<img src="https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/shredded_pork.jpg">
