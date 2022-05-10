#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *

# initialize wiimote
wiimote = Wiimote()

#Insert address and name of device here
device = ('', '')

connected = False

try:
	print "Press any key on wiimote to connect"
	while (not connected):
		connected = wiimote.Connect(device)

	print "succesfully connected"

	wiimote.SetAccelerometerMode()

	wiistate = wiimote.WiimoteState
	while True:
		# re-calibrate accelerometer
		if (wiistate.ButtonState.Home):
			print 're-calibrating'
			wiimote.calibrateAccelerometer()
			sleep(0.1)			

except KeyboardInterrupt:
	print "Exiting through keyboard event (CTRL + C)"
	exit(wiimote)
