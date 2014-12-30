#!/bin/ksh

echo "SIREN.KSH: SIREN - SIREN - SIREN"
/usr/bin/amixer -c 0 set PCM 65 2>&1 > /dev/null

## Set Defaults
configFile="/homealarm/alarm.cfg"

## Functions
getConfig() {
	if [[ -f "$configFile" ]]; then
		iterations=$(grep "numSirenLoops" $configFile | tr -d ' ' | cut -d'=' -f2)
		speakAll=$(grep "speakAll" $configFile | tr -d ' ' | cut -d'=' -f2)
	fi
	iterations=${iterations:-3}
	speakAll=${speakAll:-no}
}

getDisabled() {
	if [[ -f "$configFile" ]]; then
		disabled=$(grep "disabled" $configFile | tr -d ' ' | cut -d'=' -f2)
	fi
	disabled=${disabled:-error}
	echo $disabled
}

getConfig
loop=0

while (( $loop != $iterations )); do
	disabled=$(getDisabled)
	case $disabled in
		"error")	echo "SIREN.KSH: ERROR: Config file does not exist. Assuming disabled = 'no'.";;
		"yes")	echo "SIREN.KSH: EXITTING: Alarm has been disabled."
			exit 0;;
		"no")	echo "" > /dev/null;;
		*)	echo "SIREN.KSH: ERROR: Disabled status not correct. [DISABLED: ${disabled}]. Assuming disabled = 'no'.";;
	esac
	/usr/bin/aplay /homealarm/sounds/siren.wav 2>&1 > /dev/null
	echo "SIREN.KSH: playing siren.wav"
	if [[ $speakAll = "yes" ]]; then
		/usr/bin/espeak -a 200 -ven+m2 -k5 -s150 $1 2>&1 > /dev/null
		echo "SIREN.KSH: speaking"
	fi
	((loop++))
done

