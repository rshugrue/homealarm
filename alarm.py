#!/usr/bin/python

import logging
import logging.handlers
import subprocess
import sys, traceback
import os.path
import RPi.GPIO as GPIO
import time
from time import sleep
from datetime import datetime
import ConfigParser

## Global Variable Declaration
debug=0
config = ConfigParser.RawConfigParser()
alarmDir = "/homealarm"

# Logging Configuration
LOG_FILENAME = alarmDir + "/logs/alarm.log"
LOG_LEVEL = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=60)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
	def __init__(self, logger, level):
		self.logger = logger
		self.level = level


	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())
 
# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)
 
configFile = alarmDir + "/alarm.cfg"
logFile = alarmDir + "/logs/alarm.log"
if ( not os.path.isfile(configFile) ):
	logger.info( "FATAL ERROR: Config file ( " + configFile + " ) does not exist.")
	sys.exit(1)
if ( not os.path.isfile(logFile) ):
	logger.info( "FATAL ERROR: Config file ( " + logFile + " ) does not exist.")
	sys.exit(1)
#sys.stdout = open(logFile, 'w')
door = "Door Opened."
window = "Window Opened."
bedroom = "Bedroom Breached. Alert. Alert. Alert."
Red=""
Green=""
Blue=""

# DEFAULT SETTINGS - DO NOT EDIT
disabled = "no"
sendText = "no"
textList = []
speakZone = "yes"
speakAll = "no"
alarmZoneChanList = []
z1Pin = "na"
z2Pin = "na"
z3Pin = "na"
z4Pin = "na"
z5Pin = "na"
z6Pin = "na"
z7Pin = "na"
z8Pin = "na"
z9Pin = "na"
z10Pin = "na"
z11Pin = "na"
z12Pin = "na"
z13Pin = "na"
z14Pin = "na"
zone1 = "na"
zone2 = "na"
zone3 = "na"
zone4 = "na"
zone5 = "na"
zone6 = "na"
zone7 = "na"
zone8 = "na"
zone9 = "na"
zone10 = "na"
zone11 = "na"
zone12 = "na"
zone13 = "na"
zone14 = "na"
z1Text = "na"
z2Text = "na"
z3Text = "na"
z4Text = "na"
z5Text = "na"
z6Text = "na"
z7Text = "na"
z8Text = "na"
z9Text = "na"
z10Text = "na"
z11Text = "na"
z12Text = "na"
z13Text = "na"
z14Text = "na"
## End Global Variable Declaration

## Declare Functions
def getConfig():
	global disabled, sendText, textList, speakZone, speakAll
	global z1Pin, z2Pin, z3Pin, z4Pin, z5Pin, z6Pin, z7Pin
	global z8Pin, z9Pin, z10Pin, z11Pin, z12Pin, z13Pin, z14Pin
	global zone1, zone2, zone3, zone4, zone5, zone6, zone7
	global zone8, zone9, zone10, zone11, zone12, zone13, zone14
	global z1Text, z2Text, z3Text, z4Text, z5Text, z6Text, z7Text
	global z8Text, z9Text, z10Text, z11Text, z12Text, z13Text, z14Text
	global alarmZoneChanList
	zonePins = ""
	if ( not os.path.isfile(configFile) ):
		logger.info( "FATAL ERROR: Config file ( " + configFile + " ) does not exist.")
		sys.exit(1)
	config.read(configFile)
	disabled = config.get('Primary', 'disabled')
	sendText = config.get('Primary', 'sendtext')
	textList = config.get('Primary', 'textlist').split(",")
	if debug == 1:
		logger.debug( "textList: " + str(textList))
	speakZone = config.get('Primary', 'speakzone')
	speakAll = config.get('Primary', 'speakall')
	z1Pin, zone1, z1Text = config.get('Primary', 'zone1').split(",")
	z2Pin, zone2, z2Text = config.get('Primary', 'zone2').split(",")
	z3Pin, zone3, z3Text = config.get('Primary', 'zone3').split(",")
	z4Pin, zone4, z4Text = config.get('Primary', 'zone4').split(",")
	z5Pin, zone5, z5Text = config.get('Primary', 'zone5').split(",")
	z6Pin, zone6, z6Text = config.get('Primary', 'zone6').split(",")
	z7Pin, zone7, z7Text = config.get('Primary', 'zone7').split(",")
	z8Pin, zone8, z8Text = config.get('Primary', 'zone8').split(",")
	z9Pin, zone9, z9Text = config.get('Primary', 'zone9').split(",")
	z10Pin, zone10, z10Text = config.get('Primary', 'zone10').split(",")
	z11Pin, zone11, z11Text = config.get('Primary', 'zone11').split(",")
	z12Pin, zone12, z12Text = config.get('Primary', 'zone12').split(",")
	z13Pin, zone13, z13Text = config.get('Primary', 'zone13').split(",")
	z14Pin, zone14, z14Text = config.get('Primary', 'zone14').split(",")
	if ( not z1Pin == "na" ):
		zonePins = zonePins + z1Pin
	if ( not z2Pin == "na" ):
		zonePins = zonePins + "," + z2Pin
	if ( not z3Pin == "na" ):
		zonePins = zonePins + "," + z3Pin
	if ( not z4Pin == "na" ):
		zonePins = zonePins + "," + z4Pin
	if ( not z5Pin == "na" ):
		zonePins = zonePins + "," + z5Pin
	if ( not z6Pin == "na" ):
		zonePins = zonePins + "," + z6Pin
	if ( not z7Pin == "na" ):
		zonePins = zonePins + "," + z7Pin
	if ( not z8Pin == "na" ):
		zonePins = zonePins + "," + z8Pin
	if ( not z9Pin == "na" ):
		zonePins = zonePins + "," + z9Pin
	if ( not z10Pin == "na" ):
		zonePins = zonePins + "," + z10Pin
	if ( not z11Pin == "na" ):
		zonePins = zonePins + "," + z11Pin
	if ( not z12Pin == "na" ):
		zonePins = zonePins + "," + z12Pin
	if ( not z13Pin == "na" ):
		zonePins = zonePins + "," + z13Pin
	if ( not z14Pin == "na" ):
		zonePins = zonePins + "," + z14Pin
	alarmZoneChanList = zonePins.split(",")
	if debug == 1:
		logger.debug( "alarmZoneChanList: " + str(alarmZoneChanList))

def printConfig():
	logger.debug( "disabled: " + disabled)
	logger.debug( "sendText: " + sendText)
	logger.debug( "textList: " + str(textList))
	logger.debug( "speakZone: " + speakZone)
	logger.debug( "speakAll: " + speakAll)
	logger.debug( "z1Pin: " + z1Pin)
	logger.debug( "zone1: " + zone1)
	logger.debug( "z1Text: " + z1Text)
	logger.debug( "z2Pin: " + z2Pin)
	logger.debug( "zone2: " + zone2)
	logger.debug( "z2Text: " + z2Text)
	logger.debug( "z3Pin: " + z3Pin)
	logger.debug( "zone3: " + zone3)
	logger.debug( "z3Text: " + z3Text)
	logger.debug( "z4Pin: " + z4Pin)
	logger.debug( "zone4: " + zone4)
	logger.debug( "z4Text: " + z4Text)
	logger.debug( "z5Pin: " + z5Pin)
	logger.debug( "zone5: " + zone5)
	logger.debug( "z5Text: " + z5Text)
	logger.debug( "z6Pin: " + z6Pin)
	logger.debug( "zone6: " + zone6)
	logger.debug( "z6Text: " + z6Text)
	logger.debug( "z7Pin: " + z7Pin)
	logger.debug( "zone7: " + zone7)
	logger.debug( "z7Text: " + z7Text)
	logger.debug( "z8Pin: " + z8Pin)
	logger.debug( "zone8: " + zone8)
	logger.debug( "z8Text: " + z8Text)
	logger.debug( "z9Pin: " + z9Pin)
	logger.debug( "zone9: " + zone9)
	logger.debug( "z9Text: " + z9Text)
	logger.debug( "z10Pin: " + z10Pin)
	logger.debug( "zone10: " + zone10)
	logger.debug( "z10Text: " + z10Text)
	logger.debug( "z11Pin: " + z11Pin)
	logger.debug( "zone11: " + zone11)
	logger.debug( "z11Text: " + z11Text)
	logger.debug( "z12Pin: " + z12Pin)
	logger.debug( "zone12: " + zone12)
	logger.debug( "z12Text: " + z12Text)
	logger.debug( "z13Pin: " + z13Pin)
	logger.debug( "zone13: " + zone13)
	logger.debug( "z13Text: " + z13Text)
	logger.debug( "z14Pin: " + z14Pin)
	logger.debug( "zone14: " + zone14)
	logger.debug( "z14Text: " + z14Text)

def getZone(channel):
	if channel == int(z1Pin):
		if debug == 1:
			logger.debug( "                                         In z1Pin: ")
		zone = zone1
		text = z1Text
	elif channel == int(z2Pin):
		if debug == 1:
			logger.debug( "                                         In z2Pin: ")
		zone = zone2
		text = z2Text
	elif channel == int(z3Pin):
		if debug == 1:
			logger.debug( "                                         In z3Pin: ")
		zone = zone3
		text = z3Text
	elif channel == int(z4Pin):
		if debug == 1:
			logger.debug( "                                         In z4Pin: ")
		zone = zone4
		text = z4Text
	elif channel == int(z5Pin):
		if debug == 1:
			logger.debug( "                                         In z5Pin: ")
		zone = zone5
		text = z5Text
	elif channel == int(z6Pin):
		if debug == 1:
			logger.debug( "                                         In z6Pin: ")
		zone = zone6
		text = z6Text
	elif channel == int(z7Pin):
		if debug == 1:
			logger.debug( "                                         In z7Pin: ")
		zone = zone7
		text = z7Text
	elif channel == int(z8Pin):
		if debug == 1:
			logger.debug( "                                         In z8Pin: ")
		zone = zone8
		text = z8Text
	elif channel == int(z9Pin):
		if debug == 1:
			logger.debug( "                                         In z9Pin: ")
		zone = zone9
		text = z9Text
	elif channel == int(z10Pin):
		if debug == 1:
			logger.debug( "                                         In z10Pin: ")
		zone = zone10
		text = z10Text
	elif channel == int(z11Pin):
		if debug == 1:
			logger.debug( "                                         In z11Pin: ")
		zone = zone11
		text = z11Text
	elif channel == int(z12Pin):
		if debug == 1:
			logger.debug( "                                         In z12Pin: ")
		zone = zone12
		text = z12Text
	elif channel == int(z13Pin):
		if debug == 1:
			logger.debug( "                                         In z13Pin: ")
		zone = zone13
		text = z13Text
	elif channel == int(z14Pin):
		if debug == 1:
			logger.debug( "                                         In z14Pin: ")
		zone = zone14
		text = z14Text
	return (zone, text)

def getDisabled():
	if ( not os.path.isfile(configFile) ):
		logger.info( "FATAL ERROR: Config file ( " + configFile + " ) does not exist.")
		sys.exit(1)
	config.read(configFile)
	disabled = config.get('Primary', 'disabled')
	if ( disabled == "yes" ):
		if ( not config.has_section('Primary') ):
			config.add_section('Primary')
		config.set('Primary', 'mode', 'off')
		config.set('Primary', 'disabled', 'no')
		with open(configFile, 'w') as configFileElement:
			config.write(configFileElement)
	return disabled

def getMode():
	if ( not os.path.isfile(configFile) ):
		logger.info( "FATAL ERROR: Config file ( " + configFile + " ) does not exist.")
		sys.exit(1)
	config.read(configFile)
	mode = config.get('Primary', 'mode')
	return mode

def actOnMode(mode):
		if mode == "alarm":
			subprocess.call( alarmDir + '/siren.ksh >>' + logFile + ' 2>&1', shell=True)
			if sendText == "yes":
				for pNum in textList:
					subprocess.call('/bin/sms ' + pNum + ' ALARM IN ZONE ' + zone + ' >>' + logFile + ' 2>&1', shell=True)
			while 1:
				# Insert config read - if alarm disabled stop (break)
				disabled = getDisabled()
				if disabled == "yes":
					break
				else:
					GPIO.output(Red,GPIO.HIGH)
					GPIO.output(Green,GPIO.LOW)
					sleep(1)
					GPIO.output(Red,GPIO.LOW)
					sleep(1)
		elif mode == "alert":
			subprocess.call( alarmDir + '/beep.ksh >>' + logFile + ' 2>&1', shell=True)
		elif mode == "off":
			logger.info( str(datetime.now()) + " - Not Alerting Incident.")
		else:
			logger.info( str(datetime.now()) + " - FATAL ERROR: Event raised, but incorrect mode determined.")
			sys.exit(1)

def changeMode(mode):
	if mode == "alarm":
		houseSecure = "yes"
		for ch in alarmZoneChanList:
			if GPIO.input(int(ch)) == 0:
				zone, text = getZone(int(ch))
				logger.info( str(datetime.now()) + " - ERROR: ZONE INSECURE: " + zone)
				houseSecure = "no"
		if houseSecure == "no":
			for i in range(0, 2):
				subprocess.call( alarmDir + '/error.ksh >>' + logFile + ' 2>&1', shell=True)
			logger.info( str(datetime.now()) + " - House not secure. Unable to set mode to 'ALARM'.")
			logger.info( str(datetime.now()) + " - Resetting mode to 'ALERT'.")
			if speakZone == "yes":
				subprocess.call('/usr/bin/amixer -c 0 set PCM 80 > /dev/null 2>&1', shell=True)
				#subprocess.call('/usr/bin/espeak -a 200 -ven+m2 -k5 -s150 "Unable to set mode to. Alarm. Not all zones secure. Setting mode to. Alert." >>' + logFile + ' 2>&1', shell=True)
			# Setting configFile mode=alert
			if ( not os.path.isfile(configFile) ):
				logger.info( "FATAL ERROR: Config file ( " + configFile + " ) does not exist.")
				sys.exit(1)
			config.read(configFile)
			if ( not config.has_section('Primary') ):
                        	config.add_section('Primary')
                	config.set('Primary', 'mode', 'alert')
                	with open(configFile, 'w') as configFileElement:
                        	config.write(configFileElement)
			GPIO.output(Red,GPIO.HIGH)
			GPIO.output(Green,GPIO.HIGH)
			mode = 'alert'
		else:
			GPIO.output(Red,GPIO.HIGH)
			GPIO.output(Green,GPIO.LOW)
	elif mode == "alert":
		GPIO.output(Red,GPIO.HIGH)
		GPIO.output(Green,GPIO.HIGH)
	elif mode == "off":
		GPIO.output(Red,GPIO.LOW)
		GPIO.output(Green,GPIO.HIGH)
	else:
		logger.info( str(datetime.now()) + "INCORRECT MODE: " + mode)
		while 1:
			GPIO.output(Red,GPIO.LOW)
			GPIO.output(Green,GPIO.HIGH)
			sleep(1)
			GPIO.output(Green,GPIO.LOW)
			sleep(1)
	return mode

def my_callback(channel):
	if debug == 1:
		logger.debug( "                                      IN CALLBACK: " + str(datetime.now()))
	logger.info( str(datetime.now()) + " - Chan: " + str(channel))
	logger.info( str(datetime.now()) + " - H/L: " + str(GPIO.input(channel)))
	channelStatusOK = 0
	if debug == 1:
		logger.debug( "                                          PRE-FOR: " + str(datetime.now()))
	for i in range(1, 11):
		if GPIO.input(channel) == 1:
			channelStatusOK += 1
		sleep(.02)
	if debug == 1:
		logger.debug( "                                         POST-FOR: " + str(datetime.now()))
		logger.debug( "                                          CHANNEL: " + str(channel))
	logger.info( str(datetime.now()) + " - CHANNEL CHECK # = " + str(channelStatusOK))
	if channelStatusOK <= 6:
		zone, text = getZone(channel)
		if debug == 1:
			logger.debug( "                                          POST-IF: " + str(datetime.now()))
		logger.info( str(datetime.now()) + " - ZONE ALERT: " + zone)
		mode = getMode()
		logger.info( str(datetime.now()) + " - MODE: " + mode)
		actOnMode(mode)
		if debug == 1:
			logger.debug( "                                EXITTING CALLBACK: " + str(datetime.now()))

def main():
	global Red
	global Green
	global Blue
	if debug == 1:
		logger.debug( "                                          IN MAIN: " + str(datetime.now()))
	try:
		getConfig()
		if debug == 1:
			logger.debug(())
		if speakAll == 'yes':
			subprocess.call('/usr/bin/espeak -a 200 -ven+m2 -k5 -s150 "Alarm System Enabled." >>' + logFile + ' 2>&1', shell=True)

		GPIO.setmode(GPIO.BOARD)

		GPIO.setwarnings(False)

		## GPIO PIN ASSIGNMENT
		# Possible GPIO PINs: 11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40
		#
		# Zones(12): 11,12,13,29,31,32,33,35,36,37,38,40
		# Disable: 15
		# RGB LED: 16, 18, 22
		## END GPIO PIN ASSIGNMENT

		## Set ledChanList to the used GPIO pins for the RGB LED
		#ledChanList = [16,18,22] # Full RGB
		ledChanList = [16,18] # Only using Red & Green
		Red = 16
		Green = 18
		Blue = 22

		if debug == 1:
			logger.debug( "ZONE PIN LIST: " + str(alarmZoneChanList))

		for ch in ledChanList:
			GPIO.setup(ch, GPIO.OUT)

		for ch in alarmZoneChanList:
			GPIO.setup(int(ch), GPIO.IN)
			GPIO.add_event_detect(int(ch), GPIO.RISING, callback=my_callback, bouncetime=5000)

		if debug == 1:
			logger.debug( "                                  AFTER PIN SETUP: " + str(datetime.now()))
		mode = getMode()
		logger.info( str(datetime.now()) + " - Monitoring...   MODE: " + mode)

		try:
			while 1:
				modeRead = getMode()
				if ( not modeRead == mode ):
					changeMode(modeRead)
					modeRead = getMode()
					if ( not modeRead == mode ):
						mode = getMode()
						logger.info( str(datetime.now()) + " - MODE CHANGED TO: " + mode)
				sleep(1)

		finally:
			GPIO.cleanup()

	except KeyboardInterrupt:
		logger.info( " ")
		if debug == 1:
			logger.debug( "                                        KBRD INTR: " + str(datetime.now()))
		logger.info( str(datetime.now()) + " - Shutdown requested...exiting")
	except SystemExit:
		if sys.__stdin__.isatty():
			exit(0)
	except Exception:
		if debug == 1:
			logger.debug( "                                        EXCEPTION: " + str(datetime.now()))
		logger.info( str(datetime.now()) + " - Exception...exiting")
		traceback.print_exc(file=sys.stdout)
	else:
		if debug == 1:
			logger.debug( "                                             ELSE: " + str(datetime.now()))
		logger.info( str(datetime.now()) + " - Program End...exiting")
	if speakAll == 'yes':
		subprocess.call('/usr/bin/espeak -a 200 -ven+m2 -k5 -s150 "Alert. Alarm System Powered Down." >>' + logFile + ' 2>&1', shell=True)
	GPIO.cleanup()
	sys.exit(0)
## End Declare Functions

if __name__ == "__main__":
	if debug == 1:
		logger.debug( "                                    ENTERING MAIN: " + str(datetime.now()))
	main()
