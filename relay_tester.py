#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# init list with pin numbers
pinList = [26]

# loop through pins and set mode and state to 'high'
for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)

# time to sleep between operations in the main loop
SleepTimeL = 2

try:
    for i in pinList: 
        print("turning on")
        GPIO.output(i, GPIO.LOW)
        time.sleep(SleepTimeL); 
        print("turning off")
        GPIO.output(i, GPIO.HIGH)
        time.sleep(SleepTimeL); 
    
    GPIO.cleanup()
    print("finished cleanup")

# End program cleanly with keyboard
except KeyboardInterrupt:
    print("quit")

# Reset GPIO settings
GPIO.cleanup()