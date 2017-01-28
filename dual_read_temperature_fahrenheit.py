#!/usr/bin/python

#================================================================#
# Implemented by Michael Michael http://www.github.com/michmike
# Under MIT License
# https://raw.githubusercontent.com/michmike/Raspberry-PI-Q/master/LICENSE
#================================================================#

import smbus
import time
import datetime
import statistics

bus = smbus.SMBus(1)
THERMOCOUPLE_1_ADDRESS = 0x4f #I2C address for Robogaia dual thermocouple
THERMOCOUPLE_2_ADDRESS = 0x4c #I2C address for Robogaia dual thermocouple
MAX_SAMPLES = 10
 
def get_current_Grill_temp(): 
    try:
        data = bus.read_i2c_block_data(THERMOCOUPLE_1_ADDRESS, 1, 2)
        val = (data[0] << 8) + data[1]
        temperature = val/5.00*9.00/5.00+32.00
        return float("%.2f" % temperature)
    except Exception as e:
        print("***** Warning: Failed to gather data from device (Grill Temperature). Exception: %s" % str(e))
        raise

def get_current_Meat_temp(): 
    try:
        counter = 0
        arrayOfTemps = [None] * MAX_SAMPLES 
        while counter < MAX_SAMPLES:
            data = bus.read_i2c_block_data(THERMOCOUPLE_2_ADDRESS, 1, 2)
            val = (data[0] << 8) + data[1]
            temperature = val/5.00*9.00/5.00+32.00
            arrayOfTemps[counter] = float("%.2f" % temperature)
            counter = counter + 1
        counter = 0
        while counter < MAX_SAMPLES:
            print(arrayOfTemps[counter])
            counter = counter + 1
        print ("median_grouped " % statistics.median_grouped(arrayOfTemps))
        print ("harmonic_mean " % statistics.harmonic_mean(arrayOfTemps))
        return 
    except Exception as e:
        print("***** Warning: Failed to gather data from device (Meat Temperature). Exception: %s" % str(e))
        raise

while 1 == 1:
    grillTemp = get_current_Grill_temp()
    meatTemp = get_current_Meat_temp()
    print("temperature (grill) = %s, temperature (meat) = %s" % (grillTemp, meatTemp))
    time.sleep(1)
