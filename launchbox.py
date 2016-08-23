#!/usr/bin/env python
import os
import sys
import math
from datetime import datetime
import RPi.GPIO as GPIO
import time
import json
import urllib2
import dateutil.parser
import pytz
from pushbullet import Pushbullet
sys.path.append("/home/pi/Desktop/launchbox/Adafruit_CharLCD")
from Adafruit_CharLCD import Adafruit_CharLCD

PUSHBULLET_API_KEY = "<YOUR API KEY>"

def WriteLCDLine1(message):
    lcd.setCursor(0,0)
    lcd.message(message)

def WriteLCDLine2(message):
    lcd.setCursor(0,1)
    lcd.message(message)

def WriteLCDLine3(message):
    lcd.setCursor(0,2)
    lcd.message(message)

def WriteLCDLine4(message):
    lcd.setCursor(0,3)
    lcd.message(message)

def send_links(channel):
	#this sends a list of streaming video links as a note to
	#your pushbullet account
	global response
	links = response["launches"][0]["vidURLs"]

	linkstring = ""
	for link in links:
		linkstring = linkstring + link + "\r\n"

	WriteLCDLine4("Sending links...")
	pb = Pushbullet(PUSHBULLET_API_KEY)
	push = pb.push_note(response["launches"][0]["name"] +" Links", linkstring)
	time.sleep(1)
	WriteLCDLine4("Links sent!     ")
	time.sleep(5)
	WriteLCDLine4("                ")

#setup input pin to detect button push
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=send_links, bouncetime=200)

try:
	print "running countdown..."

	#initialize LCD
	lcd = Adafruit_CharLCD()
	lcd.begin(20,4)

	WriteLCDLine1("Retrieving launch")
	WriteLCDLine2("data...")
	
	scrollStart = 0
	loopCount = 0
	while(1):
		try:
			#get launch data
			if(loopCount == 0):
				response = json.load(urllib2.urlopen("https://launchlibrary.net/1.2/launch/next/1"))
                space = " "
				launchName = response["launches"][0]["name"] + space
           		launchSite = response["launches"][0]["location"]
                launchSite1 = launchSite["name"] + space
				launchTime = dateutil.parser.parse(response["launches"][0]["net"])
				lcd.clear()

			currentTime = datetime.utcnow().replace(tzinfo=pytz.utc)
			
            if(launchTime < currentTime):
                diff = currentTime - launchTime
			else:
				diff = launchTime - currentTime

			hours = int(diff.seconds / 3600) % 24
			minutes = int(diff.seconds / 60) % 60
			seconds = diff.seconds % 60

			#use a fancy string slicing trick to get the name to scroll
			#note the magic number 20 because the display has 20 columns
			launchNameText = launchName[scrollStart % (len(launchName) - 20) : scrollStart % len(launchName) + 20]
            launchSiteText = launchSite1[scrollStart % (len(launchSite1) - 20) : scrollStart % len(launchSite1) + 20]
			WriteLCDLine1(launchNameText[:20])
            WriteLCDLine2(launchSiteText[:20])
            WriteLCDLine3(launchTime.strftime("%m/%d/%y %H:%M:%SUTC"))
            
            if(launchTime < currentTime):
                WriteLCDLine4("T+{0}d {1}h {2}m {3}s ".format(diff.days, hours, minutes, seconds))
            else:
                WriteLCDLine4("T-{0}d {1}h {2}m {3}s ".format(diff.days, hours, minutes, seconds))
                
			scrollStart += 1
			loopCount += 1

			#this would take forever to happen, but handle it just in case
			if scrollStart == sys.maxint:
				scrollStart = 0

			#this controls the web callout, making it happen every 600 seconds
			if loopCount == 600:
				loopCount = 0
		except:
			WriteLCDLine1("Exception occured")

		time.sleep(1)

except KeyboardInterrupt:
	sys.exit()
