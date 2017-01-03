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
| Thermocouple #1 | K Type 20cm Probe Thermocouple 5ft long 0-400 celcius | $5 | https://www.amazon.com/uxcell-Probe-Thermocouple-Temperature-Sensor/dp/B008MU0SUM |
| Thermocouple #2 | K Type 20cm Probe Thermocouple 5ft long 0-400 celcius | $5 | https://www.amazon.com/uxcell-Probe-Thermocouple-Temperature-Sensor/dp/B008MU0SUM |
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
