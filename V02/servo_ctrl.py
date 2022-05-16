#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1.4                              #
#######################################################################

import gpio_class


def write(servo, pulse):
    gpio_class.write(servo, pulse)


class Motor(object):
    PWM_PIN = 1  # GPIO pin 11
    min_pulse = 100
    max_pulse = 200

    def __init__(self, servo=None):
        self.servo = servo
        return

    def set_speed(self, speed):
        speed = 11 if speed > 11 else speed
        speed = -11 if speed < -11 else speed
        speed = speed + 11
        multiplicator = speed / 22.0
        pwm = 100 * multiplicator + 100
        write(self.servo, pwm)
        return pwm

    def stop(self):
        write(self.servo, 150)


class Steering(object):
    PWM_PIN = 2  # GPIO pin 12
    min_pulse = 100
    max_pulse = 200

    def __init__(self, servo=None):
        self.servo = servo

    def set_angle(self, angle):
        angle = 45 if angle > 45 else angle
        angle = -45 if angle < -45 else angle
        angle = angle + 45
        multiplicator = angle / 90.0
        pwm = 80 * multiplicator + 115
        write(self.servo, pwm)
        return pwm

    def stop(self):
        write(self.servo, 155)
