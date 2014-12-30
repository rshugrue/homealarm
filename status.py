#!/usr/bin/python

import subprocess
import sys, traceback
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

chan_list = [11,29,31,32,33,35,36,37,38,40]

print "Channel | State"

for ch in chan_list:
	GPIO.setup(ch, GPIO.IN)
	print str(ch) + " " + str(GPIO.input(ch))
