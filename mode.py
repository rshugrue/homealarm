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
alarmDir = "/homealarm"
configFile = alarmDir + "/alarm.cfg"
if ( len(argv) > 1 ):
	script, userInput = argv
else:
	script = argv
	userInput = ""

def main():
	global config
	global userInput
	try:
		if ( not os.path.isfile(configFile) ):
			print "FATAL ERROR: Config file ( " + configFile + " ) does not exist."
			sys.exit(1)
		config.read(configFile)
		mode = str(config.get('Primary', 'mode'))
		inputTest = "invalid"
		while inputTest != "valid":
			if userInput == "":
				print "Current MODE setting: " + mode
				action = raw_input("Change mode to? [alert/alarm/off/<enter=DoNotChange>] ")
			elif userInput == "-current":
				print mode
				sys.exit(0)
			else:
				action = userInput
			if action == "alert":
				inputTest = "valid"
			elif action == "alarm":
				inputTest = "valid"
			elif action == "off":
				inputTest = "valid"
			elif action == "":
				inputTest = "valid"
			else:
				print "INVALID INPUT! Try again."
				inputTest = "invalid"
				userInput = ""
		if action == "":
			print "No action required."
		elif action == mode:
			print "No action required."
		else:
			if ( not config.has_section('Primary') ):
				config.add_section('Primary')
			config.set('Primary', 'mode', action)
			with open(configFile, 'w') as configFileElement:
				config.write(configFileElement)
			print "Alarm mode set to: " + action
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
