#!/usr/bin/python

#================================================================#
# Implemented by Michael Michael http://www.github.com/michmike
# Under MIT License
# https://raw.githubusercontent.com/michmike/Raspberry-PI-Q/master/LICENSE
#================================================================#

import time
from time import sleep
import datetime
import smtplib
import http.client
import sys
import os
import socket
import dweepy

#================ GLOBAL VARIABLES - NEED CONFIG ================#
LOGFILE = open('/tmp/Raspberry-PI-Q_startuplog.txt', 'w')
FROM_EMAIL_ADDRESS = 'raspberrypiq@gmx.com'
FROM_EMAIL_ADDRESS_PWD = 'Raspberry-pi-q17!'
TO_EMAIL_ADDRESS = 'raspberrypiq@gmx.com'
DWEET_NAME = "Raspberry-PI-Q-IPAddress"
#================ GLOBAL VARIABLES - NEED CONFIG ================#

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

def log_dweety_data(ipAddress):
    try:        
        dweepy.dweet_for(DWEET_NAME, {'ipaddress':ipAddress})        

    # check for HTTP issues and report
    except requests.HTTPError as httperror:        
        smartPrint("***** Warning: Failed to upload data to dweet.io. HTTPError({0}): {1}]".format(httperror.errno, httperror.strerror))
    except Exception as e:
        smartPrint("***** Warning: Failed to upload data to dweet.io. Exception %s" % str(e))        

#================================================================#

def smartPrint(value):
    print(value)
    LOGFILE.write(str(value) + os.linesep)

#================================================================#

def main(argv):
    try:        
        ipAddress = socket.gethostbyname(socket.gethostname())
        ipAddress2 = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        now = datetime.datetime.now()
        currentTimestamp = now.strftime("%Y-%m-%d %H:%M GMT") 
        textToSend = "Raspberry PI just rebooted at %s. My IP address is %s or %s" % (currentTimestamp, ipAddress, ipAddress2)
        smartPrint(textToSend)
        log_dweety_data(textToSend)
        send_email_or_text(textToSend,
                           TO_EMAIL_ADDRESS,
                           "notification")
    except Exception as e:
        smartPrint("***** Warning: Failed to get the IP Address or send it. Exception %s" % str(e)) 

#================================================================#

if __name__ == "__main__":
    main(sys.argv[1:])

#================================================================#
