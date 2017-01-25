#!/usr/bin/python

#================================================================#
# Implemented by Michael Michael http://www.github.com/michmike
# Under MIT License
# https://raw.githubusercontent.com/michmike/Raspberry-PI-Q/master/LICENSE
#================================================================#

import smbus
import time
import datetime


bus = smbus.SMBus(1)

#I2C address
address1 = 0x4c
address2 = 0x4f
 
 
def get_celsius_val1(): 
    data = bus.read_i2c_block_data(address1, 1,2)
    val = (data[0] << 8) + data[1]
    return val/5.00*9.00/5.00+32.00

def get_celsius_val2():
    data = bus.read_i2c_block_data(address2, 1,2)
    val = (data[0] << 8) + data[1] 
    return val/5.00*9.00/5.00+32.00

while 1 == 1:
    temperature1 = get_celsius_val1()
    temperature2 = get_celsius_val2()
    print("temperature 1 = {0:8.2f}   temperature 2 ={1:8.2f}".format(temperature1,temperature2))
    time.sleep(1)
