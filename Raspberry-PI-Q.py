#!/usr/bin/python

#================================================================#
# Implemented by Michael Michael http://www.github.com/michmike
# Under MIT License
# https://raw.githubusercontent.com/michmike/Raspberry-PI-Q/master/LICENSE
#================================================================#

import smbus
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from subprocess import call
import sys
import math
import os
import smtplib
import dweepy
import requests
import http.client
import random
import urllib.parse
import statistics

#================ GLOBAL VARIABLES - NEED CONFIG ================#
global DWEET_NAME
DWEET_NAME = '<entered through arguments>' # this is the "thing" in dweet.io language
GROWTH_RATE_RANGE = 10 # how many samples we need to have before starting to calculate the statistics for when the meat is ready
LOGFILE = open('/tmp/Raspberry-PI-Q_log.txt', 'w')
FROM_EMAIL_ADDRESS = 'raspberrypiq@gmx.com'
FROM_EMAIL_ADDRESS_PWD = 'Raspberry-pi-q17!'
global GROVE_API_KEY
GROVE_API_KEY = "<entered through arguments>"    
global GROVE_COMPONENT_ID
GROVE_COMPONENT_ID = "<entered through arguments>" # this has the same value as the DWEET_NAME
#================ GLOBAL VARIABLES - NEED CONFIG ================#

#==================== FIXED GLOBAL VARIABLES ====================#
GPIO_RELAY_FAN_PIN = 26 # this is the GPIO PIN number on the Raspberry for the Fan Relay
bus = smbus.SMBus(1)
GPIO.setmode(GPIO.BCM)
pinList = [GPIO_RELAY_FAN_PIN]
for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)

THERMOCOUPLE_1_ADDRESS  = 0x4f # I2C address for Robogaia dual thermocouple
THERMOCOUPLE_2_ADDRESS  = 0x4c # I2C address for Robogaia dual thermocouple
NUM_TEMPERATURE_SAMPLES = 10   # How many temperature samples to take to calculate harmonic mean
#==================== FIXED GLOBAL VARIABLES ====================#

#=================== OTHER GLOBAL VARIABLES  ====================#
global groveUpdateStartTime
groveUpdateStartTime = time.time()
GROVESTREAMS_UPDATE_INTERVAL_MINS = 3
#=================== OTHER GLOBAL VARIABLES  ====================#

#================================================================#

def log_grovestreams_data(currGrillTemp, currMeatTemp):
    base_url = '/api/feed?'   
    conn = http.client.HTTPConnection('www.grovestreams.com')
              
    try:            
        datapointTime = int(time.mktime(datetime.datetime.now().timetuple())) * 1000
        url = base_url + urllib.parse.urlencode({'compId' : GROVE_COMPONENT_ID, 'time' : datapointTime, 'Grill Temperature' : currGrillTemp, 'Meat Temperature' : currMeatTemp})
                    
        # The api_key token can be passed as a URL parameter or as a cookie. Passed as a cookie to keep the URL length small
        headers = {"Connection" : "close", "Content-type": "application/json", "Cookie" : "api_key=" + GROVE_API_KEY}                
        conn.request("PUT", url, "", headers)
        
        response = conn.getresponse()
        status = response.status

        # check for HTTP issues and report
        if status != 200 and status != 201:
            try:
                if response.reason != None:
                    smartPrint("***** Warning: Failed to upload data to grovestreams. HTTP Failure Reason: " + response.reason + " body: " + response.read().decode(encoding="UTF-8"))
                else:
                    smartPrint("***** Warning: Failed to upload data to grovestreams. HTTP Failure Body: " + response.read().decode(encoding="UTF-8"))
            except Exception:
                smartPrint("***** Warning: Failed to upload data to grovestreams. HTTP Failure Reason: %s" % status)
    
    except Exception as e:
        smartPrint("***** Warning: Failed to upload data to grovestreams. HTTP Failure Reason: %s" % str(e))
    
    finally:
        if conn != None:
            conn.close()   
#================================================================#

def smartPrint(value):
    print(value)
    LOGFILE.write(str(value) + os.linesep)

#================================================================#

def send_notification(currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, alertEmail, timeLeft):
    notificationText = "Raspberry-PI-Q: Grill [current=%0.2f, desired=%0.2f] -- Meat [current=%0.2f, desired=%0.2f] -- Time Left %0.2f mins" % (currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, timeLeft)
    smartPrint(notificationText)
    send_email_or_text(notificationText, alertEmail, "notification")

#================================================================#

def send_email_or_text(message, alertEmail, severity):
    try:
        TO = alertEmail
        subject = 'Raspberry-PI-Q %s' % severity
        now = datetime.datetime.now()
        currentTimestamp = now.strftime("%Y-%m-%d %H:%M GMT")
            
        formatedMessage = """From: Raspberry-PI-Q <%s>
To: %s
Subject: %s

%s
\nTime Sent: %s
""" % (FROM_EMAIL_ADDRESS, alertEmail, subject, message, currentTimestamp)
    
        server = smtplib.SMTP('mail.gmx.com:587')
        server.starttls()
        server.login(FROM_EMAIL_ADDRESS, FROM_EMAIL_ADDRESS_PWD)
        server.sendmail(FROM_EMAIL_ADDRESS, alertEmail, formatedMessage)
        server.quit()
    
    # check for issues and report
    except Exception as e:
        smartPrint("***** Warning: Failed to send email or text notification. Exception %s" % str(e)) 

#================================================================#

def log_data(currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, timeLeft):    
    global groveUpdateStartTime
    elapsedTimeForNotification = time.time() - groveUpdateStartTime
    if (elapsedTimeForNotification / 60) > GROVESTREAMS_UPDATE_INTERVAL_MINS:
        log_grovestreams_data(currGrillTemp, currMeatTemp)        
        groveUpdateStartTime = time.time() # reset the timer

    log_dweety_data(currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, timeLeft)

#================================================================#

def log_dweety_data(currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, timeLeft):
    try:      
        now = datetime.datetime.now()
        currentTimestamp = now.strftime("%Y-%m-%d %H:%M GMT")  
        dweepy.dweet_for(DWEET_NAME, {'currGrillTemp':currGrillTemp, 'desiredGrillTemp':desiredGrillTemp, 'currMeatTemp':currMeatTemp, 'desiredMeatTemp':desiredMeatTemp, 'timeLeft':"{0:.2f}".format(timeLeft), 'currentTimestamp':currentTimestamp})

    # check for HTTP issues and report
    except requests.HTTPError as httperror:        
        smartPrint("***** Warning: Failed to upload data to dweet.io. HTTPError({0}): {1}]".format(httperror.errno, httperror.strerror))
    except Exception as e:
        smartPrint("***** Warning: Failed to upload data to dweet.io. Exception %s" % str(e))        

#================================================================#

def get_current_Grill_temp(): 
    try:
        counter = 0
        totalHarmonic = 0
        arrayOfTemps = [None] * NUM_TEMPERATURE_SAMPLES 
        while counter < NUM_TEMPERATURE_SAMPLES:
            data = bus.read_i2c_block_data(THERMOCOUPLE_1_ADDRESS, 1, 2)
            val = (data[0] << 8) + data[1]
            arrayOfTemps[counter] = val/5.00*9.00/5.00+32.00            
            totalHarmonic = totalHarmonic + (1 / arrayOfTemps[counter])
            counter = counter + 1

        # since thermocouples are unreliable and can have variance in their readings
        # use the thermocouple to gather 10 samples, or NUM_TEMPERATURE_SAMPLES
        # use the samples and statistics to get the harmonic mean and the grouped median out of those values
        # average the harmonic mean and grouped median and return that as the value
        harmonicMean = NUM_TEMPERATURE_SAMPLES / totalHarmonic        
        return float("%.2f" % ((statistics.median_grouped(arrayOfTemps) + harmonicMean) / 2))
    except Exception as e:
        smartPrint("***** Warning: Failed to gather data from device (Grill Temperature). Exception: %s" % str(e))
        raise

#================================================================#

def get_current_Meat_temp(): 
    try:
        counter = 0
        totalHarmonic = 0
        arrayOfTemps = [None] * NUM_TEMPERATURE_SAMPLES 
        while counter < NUM_TEMPERATURE_SAMPLES:
            data = bus.read_i2c_block_data(THERMOCOUPLE_2_ADDRESS, 1, 2)
            val = (data[0] << 8) + data[1]
            arrayOfTemps[counter] = val/5.00*9.00/5.00+32.00            
            totalHarmonic = totalHarmonic + (1 / arrayOfTemps[counter])
            counter = counter + 1

        # since thermocouples are unreliable and can have variance in their readings
        # use the thermocouple to gather 10 samples, or NUM_TEMPERATURE_SAMPLES
        # use the samples and statistics to get the harmonic mean and the grouped median out of those values
        # average the harmonic mean and grouped median and return that as the value
        harmonicMean = NUM_TEMPERATURE_SAMPLES / totalHarmonic        
        return float("%.2f" % ((statistics.median_grouped(arrayOfTemps) + harmonicMean) / 2))
    except Exception as e:
        smartPrint("***** Warning: Failed to gather data from device (Meat Temperature). Exception: %s" % str(e))
        raise

#================================================================#

def turn_heat_on():
    try:
        smartPrint("\tRelay: Turning Fan On at %s" % datetime.datetime.now().time())
        GPIO.output(GPIO_RELAY_FAN_PIN, GPIO.LOW)        
    except Exception as e:
        smartPrint("***** Warning: Failed to interract with device (Relay On). Exception: %s" % str(e))
        raise

#================================================================#

def turn_heat_off():
    try:
        smartPrint("\tRelay: Turning Fan Off at %s" % datetime.datetime.now().time())
        GPIO.output(GPIO_RELAY_FAN_PIN, GPIO.HIGH)        
    except Exception as e:
        smartPrint("***** Warning: Failed to interract with device (Relay Off). Exception: %s" % str(e))
        raise

#================================================================#

# Info on how to calculate growth rate - http://www.wikihow.com/Calculate-Growth-Rate
def calculate_time_left(arrayIndex, currMeatTemp, desiredMeatTemp, historicalTemps, loopInterval):
    if currMeatTemp > desiredMeatTemp:
        return 0

    totalOfAllGrowthAverages = 0
    trueIndex = arrayIndex % GROWTH_RATE_RANGE
    for x in range(trueIndex+1, trueIndex+GROWTH_RATE_RANGE):
        # if any of the values have not been defined yet, return 999 to indicate timer is not set yet
        if (historicalTemps[x % GROWTH_RATE_RANGE] is None):
            return 999
        growthRatePercentage = (historicalTemps[(x + 1) % GROWTH_RATE_RANGE] / historicalTemps[x % GROWTH_RATE_RANGE]) - 1 # (temp_present/temp_past)^(1/n)- 1...In this case, we are using only 1 sample, so n=1
        totalOfAllGrowthAverages += growthRatePercentage
    averageGrowthOverTime = totalOfAllGrowthAverages / (GROWTH_RATE_RANGE - 1); # we calculated it over N-1 periods for the N=GROWTH_RATE_RANGE temperature values

    if averageGrowthOverTime == 0:
        # log(1) = 0 and we can't have that. Assume 1 degree increase of some sorts
        averageGrowthOverTime = 0.01

    numberOfIntervals = (math.log(desiredMeatTemp / currMeatTemp))/(math.log(averageGrowthOverTime + 1)) # n = log(temp_future/temp_present)/log(growth rate + 1)
    timeLeft = (numberOfIntervals * loopInterval) / 60 # time left in minutes
    return abs(timeLeft) # account for negative growth in some numbers

#================================================================#

# Loop to run the fan continuously until we reach the setup temperature
def PID_Setup_Loop(grillSetupTemp, alertEmail, alertFrequency):
    current_temp = float(get_current_Grill_temp())
    heater_state = "off"
    turn_heat_off() # as a precaution, turn fan off before we begin. this is incase we encountered an exception that left the relay on
    smartPrint("Entering Setup Loop until we reach %0.2f degrees fahrenheit. Current temperature is %0.2f" % (grillSetupTemp, current_temp))
    notificationStartTime = time.time()
    while grillSetupTemp > current_temp:
        current_temp = float(get_current_Grill_temp())
        log_data(current_temp, grillSetupTemp, 999, 999, 999)
        
        # check to see if we need to send a notification
        elapsedTimeForNotification = time.time() - notificationStartTime
        if (elapsedTimeForNotification / 60) > alertFrequency:
            send_notification(current_temp, grillSetupTemp, 999, 999, alertEmail, 999)
            notificationStartTime = time.time() # reset the timer

        if heater_state == "off":
            heater_state = "on"
            smartPrint("Turning Fan ON until we reach %0.2f. Current temperature is %0.2f" % (grillSetupTemp, current_temp))
            turn_heat_on()
        else:
            smartPrint("Leaving the Fan ON until we reach %0.2f. Current temperature is %0.2f" % (grillSetupTemp, current_temp))
        sleep(10)

    # we reached our desired temperature. time to turn off the fan and exit
    current_temp = float(get_current_Grill_temp())
    if heater_state == "on":
        heater_state = "off"
        smartPrint("Turning Fan OFF since we reached or exceeded %0.2f. Current temperature is %0.2f" % (grillSetupTemp, current_temp))
        turn_heat_off()

#================================================================#

def PID_Control_Loop(desiredGrillTemp, desiredMeatTemp, alertEmail, alertFrequency, loopInterval):
    arrayIndex = 0
    historicalTemps = [None] * GROWTH_RATE_RANGE    
    heater_state = "off"
    currMeatTemp = float(get_current_Meat_temp())
    currGrillTemp = float(get_current_Grill_temp())    
    smartPrint("Entering Control Loop with Grill [now=%0.2f, desired=%0.2f] -- Meat [now=%0.2f, desired=%0.2f]" % (currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp))
        
    # This while loop will never end
    notificationStartTime = time.time()
    tempAlertStartTime = time.time()
    while True:
        startTime = time.time()
        currMeatTemp = float(get_current_Meat_temp())
        currGrillTemp = float(get_current_Grill_temp())
        
        difference = desiredGrillTemp - currGrillTemp
        if (difference < 0):
            leaveTheFanOnTime = 0
        else:
            leaveTheFanOnTime = math.log(difference)

        historicalTemps[(arrayIndex % GROWTH_RATE_RANGE)] = currMeatTemp
        timeLeft = calculate_time_left(arrayIndex, currMeatTemp, desiredMeatTemp, historicalTemps, loopInterval)
        
        smartPrint("Readings: Grill [now=%0.2f, desired=%0.2f] -- Meat [now=%0.2f, desired=%0.2f] -- Fan for ~%d secs -- Time Left %0.2f mins" % (currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, leaveTheFanOnTime, timeLeft))
        log_data(currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, timeLeft)

        # check to see if we need to send a notification
        elapsedTimeForNotification = time.time() - notificationStartTime
        if (elapsedTimeForNotification / 60) > alertFrequency:
            send_notification(currGrillTemp, desiredGrillTemp, currMeatTemp, desiredMeatTemp, alertEmail, timeLeft)
            notificationStartTime = time.time() # reset the timer

        if difference <= 3 and difference >= -3:
            # don't provide any air at all as we are close to our optimal temperature
            smartPrint("We are close to our desired temperature for the Grill. Do Nothing!")
        elif difference < -3:
            notificationText = "***** Warning: We are above the desired temperature for the grill by more than 3 degrees. Rapsberry-PI-Q will try to recover, but PLEASE KEEP THIS IN MIND!"
            smartPrint(notificationText)            
            elapsedTimeForNotification = time.time() - tempAlertStartTime
            if (elapsedTimeForNotification / 60) > alertFrequency:
                send_email_or_text(notificationText, alertEmail, "warning")
                tempAlertStartTime = time.time() # reset the timer

        elif difference > 3:
            if heater_state == "off":
                heater_state = "on"
                turn_heat_on()
            else:
                smartPrint("Leaving the Heat ON")
            sleep(leaveTheFanOnTime)

        if heater_state == "on":
            heater_state = "off"
            turn_heat_off()
        else:
            smartPrint("Leaving the Heat OFF")

        elapsedTime = time.time() - startTime  # elapsedTime is in seconds and it accounts for the time spend with the fan on
        if elapsedTime > loopInterval:
            # we have a problem here since it is taking longer to run the loop. sleep a token 5 seconds
            notificationText = "***** Warning: The chosen loop interval of %d seconds is too small. Consider increasing the inverval to over %d seconds" % (loopInterval, elapsedTime)
            smartPrint(notificationText)
            elapsedTimeForNotification = time.time() - tempAlertStartTime
            if (elapsedTimeForNotification / 60) > alertFrequency:
                send_email_or_text(notificationText, alertEmail, "warning")
                tempAlertStartTime = time.time() # reset the timer

            sleep(5)
        else:
            sleep(loopInterval - elapsedTime)  # sleep the remainder seconds to allow temperature to stabilize after the loop
        arrayIndex = arrayIndex + 1
        
#================================================================#

def main(argv):    
    if len(sys.argv) < 9:
        smartPrint("Usage: Raspberry-PI-Q.py [setup temperature to reach with continuous air] [grill temperature] [meat temperature] [alert email] [frequency of notifications in minutes] [loop interval in seconds; recommended 60] [unique name for your device; like Raspberry-PI-Q-Michael] [secret API key for grovestreams] &")
        # example: sudo python3 Raspberry-PI-Q.py 180 225 125 email@address.com 5 30 Raspberry-PI-Q-Michael groove-api-guid &
        # ATT email-to-text is 10digitphonenumber@txt.att.net
        # TMobile email-to-text is 10digitphonenumber@tmomail.net

        sys.exit(1)        
    try:
        grillSetupTemp=float(sys.argv[1])
        desiredGrillTemp=float(sys.argv[2])
        desiredMeatTemp=float(sys.argv[3])
        alertEmail=sys.argv[4]
        alertFrequency=float(sys.argv[5])
        loopInterval=float(sys.argv[6])
        global DWEET_NAME
        DWEET_NAME = sys.argv[7]
        global GROVE_COMPONENT_ID
        GROVE_COMPONENT_ID = sys.argv[7] # notice this is the same value as the DWEET_NAME
        global GROVE_API_KEY
        GROVE_API_KEY = sys.argv[8]

        global groveUpdateStartTime
        groveUpdateStartTime = time.time() # reset the timer
        
    except ValueError:
        smartPrint("One of the arguments was invalid")
        smartPrint("Usage: Raspberry-PI-Q.py [setup temperature to reach with continuous air] [grill temperature] [meat temperature] [alert email] [frequency of notifications in minutes] [loop interval in seconds; recommended 60] [unique name for your device; like Raspberry-PI-Q-Michael] [secret API key for grovestreams]")
        sys.exit(1)
    smartPrint("grillSetupTemp=%d, desiredGrillTemp=%d, desiredMeatTemp=%d, alertEmail=%s, alertFrequency=%d, loopInterval=%d, DWEET_NAME=%s, GROVE_API_KEY=%s" % (grillSetupTemp, desiredGrillTemp, desiredMeatTemp, alertEmail, alertFrequency, loopInterval, DWEET_NAME, GROVE_API_KEY))
    
    try:        
        PID_Setup_Loop(grillSetupTemp, alertEmail, alertFrequency)
        PID_Control_Loop(desiredGrillTemp, desiredMeatTemp, alertEmail, alertFrequency, loopInterval)
    except KeyboardInterrupt:
        smartPrint("Exiting after a keyboard cancellation...Goodbye...")
    except Exception as excp:
        smartPrint("***** Alert: An exception occured in running the setup or control loops. Trying again. Error: %s" % excp)
        send_email_or_text("An error happened while running the automatic temperature control. Rapsberry-PI-Q will try to recover, but PLEASE COME AND MONITOR YOUR GRILL IMMEDIATELY!", alertEmail, "alert")
        smartPrint("Running program again in 10 seconds")
        for x in range(1,10):
            smartPrint(x)
            sleep(1)
        main(sys.argv[1:])
    finally:
        GPIO.cleanup()

#================================================================#

if __name__ == "__main__":
    main(sys.argv[1:])

#================================================================#