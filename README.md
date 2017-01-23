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
* Help on wiring the relay
  * https://www.amazon.com/gp/customer-reviews/RUNBAXRMMUMBL/ref=cm_cr_arp_d_rvw_ttl?ie=UTF8&ASIN=B00KTEN3TM
  * https://www.youtube.com/watch?v=OQyntQLazMU

## Source Code




## Pictures
![Relay and Power Wiring](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_001929.jpg)
![Fan](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002004.jpg)
![Wiring of Ground, VCC, and Relay #2](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002454.jpg)
![Robogaia board pass-through connection to 5v power and ground](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002514.jpg)
![Thermocouples on the robogaia dual board](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002521.jpg)
![GPIO 26 connection to the relay #2](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/IMG_20170123_002602.jpg)
![PIN layout for Raspberry](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/RaspberryPI2_PIN_layout.jpg)
![PIN layout for Raspberry](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/RaspberryPI3_PIN_layout.jpg)
![Example email alert](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/email-alert.png)
![Fan adaptor to fit Big Green Egg style grills](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/fan-adaptor-for-big-green-egg.jpg)
![Inactivity outside-in monitoring alert](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/outside-in-monitoring.png)
![Parts](https://github.com/michmike/Raspberry-PI-Q/blob/master/Images/parts.jpg)




