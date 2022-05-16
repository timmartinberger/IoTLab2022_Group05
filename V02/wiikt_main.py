#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *
from servo_ctrl import Motor, Steering
import threading

# initialize wiimote
wiimote = Wiimote()

#Insert address and name of device here
device = ('2C:10:C1:BE:45:1D', 'Nintendo RVL-CNT-01-TR')

connected = False

# initialize the controls
MAX_VELOCITY = 11
MAX_DEFLECTION = 45

control_boundaries = {
	'velocity': MAX_VELOCITY,
	'deflection': MAX_DEFLECTION,
}
velocity_step = 1
deflection_step = 5

# initialize the servo controls

motor = Motor(1)
steering = Steering(2)

# utility functions

def indicate_speed(wiimote, speed):
	if 0 <= speed < 3:
		wiimote.SetLEDs(False, False, False, False)
	elif 3 <= speed < 6:
		wiimote.SetLEDs(True, False, False, False)
	elif 6 <= speed < 9:
		wiimote.SetLEDs(True, True, False, False)
	elif 9 <= speed < MAX_VELOCITY:
		wiimote.SetLEDs(True, True, True, False)
	else:
		wiimote.SetLEDs(True, True, True, True)


def calculate_pitch(wiistate):
	accel_x = wiistate.AccelState.RawZ
	normalized =  1 * accel_x / 102.0
	angle = 90 * normalized
	return angle

def calculate_steering(wiistate):
	accel_y = wiistate.AccelState.RawY
	normalized = -1 * accel_y / 102.0
	angle = 90 * normalized
	return angle

def set_speed_from_angle(angle, max_angle, max_velocity, control_boundaries):
	normalized = angle / max_angle
	speed = round(abs(normalized * max_velocity))
	print speed
	control_boundaries['velocity'] = speed


class SteeringThread(threading.Thread):

	def __init__(self, wiistate, steering, control_boundaries, low_pass = False):
		threading.Thread.__init__(self)
		self.wiistate = wiistate
		self.steering = steering
		self.control_boundaries = control_boundaries
		self.low_pass = low_pass


	def run(self):
		last_steering_angle = 0
		omega = 0.1
		while True:
			steering_angle = calculate_steering(self.wiistate)
			if self.low_pass:
				# apply exponential smoothing
				steering_angle = omega * steering_angle + (1 - omega) * last_steering_angle
				last_steering_angle = steering_angle

			if steering_angle >= 0:
				steering_angle = min(steering_angle, self.control_boundaries['deflection'])
				print steering_angle
				steering.set_angle(steering_angle)
			else:
				steering_angle = max(steering_angle, -self.control_boundaries['deflection'])
				print steering_angle
				steering.set_angle(steering_angle)
			
			sleep(0.1)
			

		

try:
	print "Press any key on wiimote to connect"
	while (not connected):
		connected = wiimote.Connect(device)

	print "succesfully connected"

	wiimote.SetAccelerometerMode()

	wiistate = wiimote.WiimoteState

	sleep_time = 0.1

	steering_thread = SteeringThread(wiistate, steering, control_boundaries, low_pass=True)

	steering_thread.start()
	while True:
		indicate_speed(wiimote=wiimote, speed=control_boundaries['velocity'])


		# re-calibrate accelerometer
		if (wiistate.ButtonState.Home):
			print 're-calibrating'
			wiimote.calibrateAccelerometer()
			sleep(sleep_time)

		# pitch
		if (wiistate.ButtonState.Plus):
			pitch = calculate_pitch(wiistate)
			set_speed_from_angle(pitch, 90.0, MAX_VELOCITY, control_boundaries)
			sleep(sleep_time)
		
		### Steuerkreuz

		if (wiistate.ButtonState.Right):
			if (control_boundaries['velocity'] == MAX_VELOCITY):
				print 'velocity set to max'
			elif 0 <= control_boundaries['velocity'] < MAX_VELOCITY:
				control_boundaries['velocity'] += velocity_step
				print control_boundaries['velocity']
			sleep(sleep_time)

		if (wiistate.ButtonState.Left):
			if control_boundaries['velocity'] == 0:
				print 'velocity set to zero'
			if 0 < control_boundaries['velocity'] <= MAX_VELOCITY:
				control_boundaries['velocity'] -= velocity_step
				print control_boundaries['velocity']
			sleep(sleep_time)

		if (wiistate.ButtonState.Up):
			if control_boundaries['deflection'] == 0:
				print 'deflection set to zero'
			elif 0 < control_boundaries['deflection'] <= MAX_DEFLECTION:
				control_boundaries['deflection'] -= deflection_step
				print control_boundaries['deflection']
			sleep(sleep_time)

		if (wiistate.ButtonState.Down):
			if control_boundaries['deflection'] == MAX_DEFLECTION:
				print 'deflection set to max'
			elif 0 <= control_boundaries['deflection'] < MAX_DEFLECTION:
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

		### reset 
		if (wiistate.ButtonState.Minus):
			print 'reset'
			control_boundaries['deflection'] = 0
			control_boundaries['velocity'] = 0
			sleep(sleep_time)
	stearing_thread.join()



except KeyboardInterrupt:
	print "Exiting through keyboard event (CTRL + C)"
	exit(wiimote)
