#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *
from servo_ctrl import Motor, Steering

# initialize wiimote
wiimote = Wiimote()

#Insert address and name of device here
device = ('2C:10:C1:BE:45:1D', 'Nintendo RVL-CNT-01-TR')

connected = False

# initialize the controls
max_velocity = 11
max_deflection = 45

control_boundaries = {
	'velocity': max_velocity,
	'deflection': max_deflection,
}
velocity_step = 1
deflection_step = 5

# initialize the servo controls

motor = Motor(1)
steering = Steering(2)

# utility functions

def indicate_speed(wiimote: Wiimote, speed: int):
	if speed == 0:
		wiimote.SetLEDs(False, False, False, False)
	elif 0 < speed < 3:
		wiimote.SetLEDs(True, False, False, False)
	elif 3 < speed < 6:
		wiimote.SetLEDs(True, True, False, False)
	elif 6 < speed < 9:
		wiimote.SetLEDs(True, True, True, False)
	else:
		wiimote.SetLEDs(True, True, True, True)

try:
	print "Press any key on wiimote to connect"
	while (not connected):
		connected = wiimote.Connect(device)

	print "succesfully connected"

	wiimote.SetAccelerometerMode()

	wiistate = wiimote.WiimoteState

	sleep_time = 0.1
	while True:
		# re-calibrate accelerometer
		if (wiistate.ButtonState.Home):
			print 're-calibrating'
			wiimote.calibrateAccelerometer()
			sleep(sleep_time)

		### Steuerkreuz

		if (wiistate.ButtonState.Right):
			if (control_boundaries['velocity'] == max_velocity):
				print 'velocity set to max'
			elif 0 <= control_boundaries['velocity'] < max_velocity:
				control_boundaries['velocity'] += velocity_step
				print control_boundaries['velocity']
			sleep(sleep_time)

		if (wiistate.ButtonState.Left):
			if control_boundaries['velocity'] == 0:
				print 'velocity set to zero'
			if 0 < control_boundaries['velocity'] <= max_velocity:
				control_boundaries['velocity'] -= velocity_step
				print control_boundaries['velocity']
			sleep(sleep_time)

		if (wiistate.ButtonState.Up):
			if control_boundaries['deflection'] == 0:
				print 'deflection set to zero'
			elif 0 < control_boundaries['deflection'] <= max_deflection:
				control_boundaries['deflection'] -= deflection_step
				print control_boundaries['deflection']
			sleep(sleep_time)

		if (wiistate.ButtonState.Down):
			if control_boundaries['deflection'] == max_deflection:
				print 'deflection set to max'
			elif 0 <= control_boundaries['deflection'] < max_deflection:
				control_boundaries['deflection'] += deflection_step
				print control_boundaries['deflection']
			sleep(sleep_time)

		### forward backward

		if (wiistate.ButtonState.One):
			print 'forward'
			motor.set_speed(control_boundaries['velocity'])
			sleep(sleep_time)
		
		if (wiistate.ButtonState.Two):
			print 'backward'
			motor.set_speed(-control_boundaries['velocity'])
			sleep(sleep_time)




except KeyboardInterrupt:
	print "Exiting through keyboard event (CTRL + C)"
	exit(wiimote)
