#!/usr/bin/python

import subprocess
import os.path
import sys
import traceback
from sys import argv
import time
from time import sleep
from datetime import datetime
import ConfigParser

## Global Variable Declaration
config = ConfigParser.RawConfigParser()
if ( len(argv) > 1 ):
	script, userInput = argv
else:
	script = argv
	userInput = "invalid"
alarmDir = "/homealarm"
configFile = alarmDir + "/alarm.cfg"

def main():
	global config
	global userInput
	try:
		if ( not os.path.isfile(configFile) ):
			print "FATAL ERROR: Config file ( " + configFile + " ) does not exist."
			sys.exit(1)
		config.read(configFile)
		if userInput == "":
			answer = raw_input("Disable Alarm? [yes/NO] ")
		else:
			answer = userInput
		if answer == "yes":
			if ( not config.has_section('Primary') ):
				config.add_section('Primary')
			config.set('Primary', 'disabled', answer)
			with open(configFile, 'w') as configFileElement:
				config.write(configFileElement)
			print "Alarm Disabled: " + answer
		else:
			print "Alarm NOT Disabled."
		sys.exit(0)
	except KeyboardInterrupt:
		#print " "
		print "Shutdown requested...exiting"
	except Exception:
		#print " "
		print "Exception...exiting"
		traceback.print_exc(file=sys.stdout)
	else:
		#print "Program End...exiting"
		print ""
	sys.exit(0)

if __name__ == "__main__":
	main()
