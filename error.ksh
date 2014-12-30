#!/bin/ksh

echo "ERROR-BEEP"
/usr/bin/amixer -c 0 set PCM 80 2>&1 > /dev/null
/usr/bin/aplay /homealarm/sounds/doorbeep.wav 2>&1 > /dev/null
