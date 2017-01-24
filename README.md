# Raspberry-PI-Q
Heavily influenced by @justindean and his [PitmasterPI](https://github.com/justindean/PitmasterPi) project, I decided to create an advanced BBQ temperature controller using a Raspberry PI (RPI). The goals of the project were the following:
* Make delicious and consistently great BBQ
* Use RPI to control the fan and thus the temperature of the charcoal
* Use RPI and predictive algorithms to let me know the exact time when my meat will reach the desired temperature
* Use RPI and email/text notifications if my desired intent is not met
* Make it affordable
* Create cool dashboards to show off my cooking

The biggest difference of this project from the one @justindean created is the fact that i wanted to be able to have two thermocouples so that i can also monitor the temperature of the meat. Using simple growth rate math, I can use all these data to predict when my BBQ would reach the desired temperature. The updated BOM is listed below.

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

## Wiring Diagram
* Connect the Robogaia dual thermocouple plate
* Connect the relay	
  * Useful post: https://www.amazon.com/gp/customer-reviews/RUNBAXRMMUMBL/ref=cm_cr_arp_d_rvw_ttl?ie=UTF8&ASIN=B00KTEN3TM
  * Useful video: https://www.youtube.com/watch?v=OQyntQLazMU
  * There are two rows of input pins (GND IN1 IN2 IN3 IN4 VCC) and (JD-VCC VCC) with the latter coming with a jumper bridging the pins (keep the jumper on!)
	  * Connect a wire from GND on your device (pin #6) to GND on the relay module
	  * Connect a wire from the 5V pin on your device (pin #2) to the VCC pin that is adjacent to IN4 (not the one next to JD-VCC!)
	  * Finally hook the GPIO 26 (pin #37) up to IN2 
	  * Set the pin to 'low' or 0V in the software to activate and 'high' or 3.3V-5V to deactivate
	sudo python3 relay_tester.py
 
## Setting up the Raspberry PI 3 Model B
You only need to perform the following steps once!


## Development Instructions
* Install Python for Windows
* Install Visual Studio Code with the python extension from https://marketplace.visualstudio.com/items?itemName=donjayamanne.python
* Install PIP as per instructions from https://pip.pypa.io/en/stable/installing/
* Create an account with www.dweet.io and www.freeboard.io. You don't need to pay for a locked object. You can create your own board and save it with your own dashboard analytics for this project
* Create an account with www.gmx.com to get a free email address
* Create an account with www.grovestreams.com. 
  * Create an organization and under advanced enable the "Raspberry PI Metrics" blueprint
  * For more details, read https://www.grovestreams.com/developers/getting_started_rpi.html
  * Once your account is created, go to the Dashboard and click on Admin>API Keys>Click on Feed Put API Key>View Secret Key. You need to save this key as this is needed as input to the Raspberry-PI-Q
  * For your streams\components, create at least two notifications via email (free). When you create the notification, make sure to select an "Action Package" 
		 * A value condition event notification so that you are notified if your meat or grill falls out of any specific ranges
		 * A latency event so that you are notified immediately if data is not coming from the RPI, which means something went wrong. This is a very simplistic type of outside-in monitoring


## Source Code
| File | Description |
| ------------- | ---- |
| Raspberry-PI-Q.py | |
| index.html | |
| launcher.py | |
| email_IP_address.py | |
| Freeboard_HTML_MeatChart.txt | |
| Freeboard_HTML_Dashboard | | 
| relay_tester.py | |
| dual_read_temperature_fahrenheit.py | |

## Startup Operations
Perform these steps every time you grill!


## Future Ideas
Some things I want to explore for a v2 of this project include
* Use most of the same hardware to create a sous vide immersion circulator
* Add a high-heat camera to take pictures of my meat _inside_ the grill
* Adopt the Facebook Messenger Bot architecture to create a bot for my Raspberry-PI-Q

## Pictures
1. Relay and Power Wiring
![Relay and Power Wiring](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_001929.jpg)
2. Fan
![Fan](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002004.jpg)
3.Wiring of Ground, VCC, and Relay #2 
![Wiring of Ground, VCC, and Relay #2](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002454.jpg)
4. Robogaia board pass-through connection to 5v power and ground
![Robogaia board pass-through connection to 5v power and ground](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002514.jpg)
5. Thermocouples on the robogaia dual board
![Thermocouples on the robogaia dual board](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002521.jpg)
6. GPIO 26 connection to the relay #2
![GPIO 26 connection to the relay #2](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002602.jpg)
7. PIN layout for Raspberry
![PIN layout for Raspberry](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/RaspberryPI2_PIN_layout.jpg)
8. PIN layout for Raspberry
![PIN layout for Raspberry](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/RaspberryPI3_PIN_layout.jpg)
9. Example email alert
![Example email alert](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/email-alert.png)
10. Fan adaptor to fit Big Green Egg style grills
![Fan adaptor to fit Big Green Egg style grills](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/fan-adaptor-for-big-green-egg.jpg)
11. Inactivity outside-in monitoring alert
![Inactivity outside-in monitoring alert](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/outside-in-monitoring.png)
12. Parts 
![Parts](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/parts.jpg)
