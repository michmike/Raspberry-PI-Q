#!/usr/bin/python

#================================================================#
# Implemented by Michael Michael http://www.github.com/michmike
# Under MIT License
# https://raw.githubusercontent.com/michmike/Raspberry-PI-Q/master/LICENSE
#================================================================#

import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

# init list with pin numbers
pinList = [26]

# loop through pins and set mode and state to 'high'
for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)

# time to sleep in seconds between operations in the main loop
SleepTimeL = 20

# If a parameter is passed to end this script after a certain time, go ahead and execute on it
# Time is passed in seconds
if len(sys.argv) > 1:
    startTime = time.time()
    endTime = float(sys.argv[1])

try:
    while 1 == 1:
        for i in pinList: 
            print("turning on")
            GPIO.output(i, GPIO.LOW)
            time.sleep(SleepTimeL); 
            print("turning off")
            GPIO.output(i, GPIO.HIGH)
            time.sleep(SleepTimeL); 
        if len(sys.argv) > 1:
            elapsedTimeForNotification = time.time() - startTime
            if elapsedTimeForNotification > endTime:
                break
except KeyboardInterrupt:
    print("Exiting after a keyboard cancellation...Goodbye...")
finally:    
    GPIO.cleanup()
    print("Finished cleanup of GPIO")