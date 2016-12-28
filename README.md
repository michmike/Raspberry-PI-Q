# Raspberry-PI-Q
Heavily influenced by @justindean and his [PitmasterPI](https://github.com/justindean/PitmasterPi) project, I decided to create an advanced BBQ temperature controller using a Raspberry PI (RPI). The goals of the project were the following:
1. Make delicious and consistently great BBQ
2. Use RPI to control the fan and thus the temperature of the charcoal
3. Use RPI and predictive algorithms to let me know the exact time when my meat will reach the desired temperature
4. Use RPI and email/text notifications if my desired intent is not met
5. Make it affordable
6. Create cool dashboards to show off my cooking

The biggest difference of this project from the one @justindean created is the fact that i wanted to be able to have two thermocouples so that i can also monitor the temperature of the meat. Using simple growth rate math, I can use all these data to predict when my BBQ would reach the desired temperature. The updated BOM is listed below.

## Bill of Materials (BOM)

| Functionality | Item | Price | Link |
| ------------- | ---- | ----- | ---- |
| Computer | Raspberry Pi 3 Model B Motherboard | $40 | https://www.amazon.com/Raspberry-Pi-RASP-PI-3-Model-Motherboard/dp/B01CD5VC92 |
| Power Supply | 5V 2.5A power supply  | $10 | https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Charger/dp/B00MARDJZ4 |
| Memory | Samsung 16GB microSDHC Class 6 | $10 | https://www.amazon.com/Samsung-Electronics-microSDHC-MB-MSAGB-AM/dp/B009SK599U |
| Fan | DC 12V 0.15A Squirrel Cage brushless fan | $9 | https://www.amazon.com/Connector-Cooling-Blower-50mmx15mm-Laptop/dp/B00MJU6JR2 |
| Thermocouple #1 | K Type 20cm Probe Thermocouple 5ft long 0-400 celcius | $5 | https://www.amazon.com/uxcell-Probe-Thermocouple-Temperature-Sensor/dp/B008MU0SUM |
| Thermocouple #2 | K Type 20cm Probe Thermocouple 5ft long 0-400 celcius | $5 | https://www.amazon.com/uxcell-Probe-Thermocouple-Temperature-Sensor/dp/B008MU0SUM |
| Thermocouple Plate | Dual Thermocouple Plate for Raspberry | $50 | http://www.robogaia.com/raspberry-pi-dual-thermocouple-plate.html |
| Relay | 4-channel DC 5V Relay Module AC250V/10A, DC30V/10A | $7 | https://www.amazon.com/JBtek-Channel-Module-Arduino-Raspberry/dp/B00KTEN3TM |
| Wiring | Female to Female 1P-1P jumper cables, 100 pcs | $8 | https://www.amazon.com/SUNKEE-100pcs-female-jumper-Dupont/dp/B00AYCON8Y |

## Wiring Diagram


## Source Code


## Pictures
