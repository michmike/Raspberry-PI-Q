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
import sys

bus = smbus.SMBus(1)
THERMOCOUPLE_1_ADDRESS = 0x4f # I2C address for Robogaia dual thermocouple
THERMOCOUPLE_2_ADDRESS = 0x4c # I2C address for Robogaia dual thermocouple
MAX_SAMPLES = 10
 
def get_current_Grill_temp(): 
    try:
        counter = 0
        totalHarmonic = 0
        arrayOfTemps = [None] * MAX_SAMPLES 
        while counter < MAX_SAMPLES:
            data = bus.read_i2c_block_data(THERMOCOUPLE_1_ADDRESS, 1, 2)
            val = (data[0] << 8) + data[1]
            arrayOfTemps[counter] = val/5.00*9.00/5.00+32.00            
            totalHarmonic = totalHarmonic + (1/arrayOfTemps[counter])
            counter = counter + 1

        harmonicMean = MAX_SAMPLES / totalHarmonic        
        return float("%.2f" % ((statistics.median_grouped(arrayOfTemps) + harmonicMean) / 2))
    except Exception as e:
        print("***** Warning: Failed to gather data from device (Grill Temperature). Exception: %s" % str(e))
        raise

def get_current_Meat_temp(): 
    try:
        counter = 0
        totalHarmonic = 0
        arrayOfTemps = [None] * MAX_SAMPLES 
        while counter < MAX_SAMPLES:
            data = bus.read_i2c_block_data(THERMOCOUPLE_2_ADDRESS, 1, 2)
            val = (data[0] << 8) + data[1]
            arrayOfTemps[counter] = val/5.00*9.00/5.00+32.00            
            totalHarmonic = totalHarmonic + (1/arrayOfTemps[counter])
            counter = counter + 1

        harmonicMean = MAX_SAMPLES / totalHarmonic        
        return float("%.2f" % ((statistics.median_grouped(arrayOfTemps) + harmonicMean) / 2))
    except Exception as e:
        print("***** Warning: Failed to gather data from device (Meat Temperature). Exception: %s" % str(e))
        raise

# If a parameter is passed to end this script after a certain time, go ahead and execute on it
# Time is passed in seconds
if len(sys.argv) > 1:
    startTime = time.time()
    endTime = float(sys.argv[1])
    print("Starting dual_read_temperature_fahrenheit.py to test the thermocouples for %s seconds" % endTime)

while 1 == 1:
    grillTemp = get_current_Grill_temp()
    meatTemp = get_current_Meat_temp()
    print("temperature (grill) = %s, temperature (meat) = %s" % (grillTemp, meatTemp))
    time.sleep(1)
    if len(sys.argv) > 1:
        elapsedTimeForNotification = time.time() - startTime
        if elapsedTimeForNotification > endTime:
            break
