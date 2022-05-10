#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1.3                              #
#######################################################################

import gpio_class

def write(servo, pulse):
    gpio_class.write(servo, pulse)

class Motor(object):
    PWM_PIN = 1     # GPIO pin 11
    min_pulse = 100
    max_pulse = 200
    def __init__(self, servo=None):
        return
    def set_speed(self, speed):
        return
    def stop(self):
        return

class Steering(object):
    PWM_PIN = 2     # GPIO pin 12
    min_pulse = 100
    max_pulse = 200
    def __init__(self, servo=None):
        return
    def set_angle(self, angle):
        return
    def stop(self):
        return
