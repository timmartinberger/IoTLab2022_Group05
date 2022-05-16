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
        speed = speed + 11
        multiplicator = speed / 22
        write(self.servo, 100 * multiplicator + 100)

        # if speed == -11:
        #     write(self.servo, 100)
        # elif speed == 11:
        #     write(self.servo, 200)
        # else:
        #     write(self.servo, 150)

    def stop(self):
        write(self.servo, 150)


class Steering(object):
    PWM_PIN = 2  # GPIO pin 12
    min_pulse = 100
    max_pulse = 200

    def __init__(self, servo=None):
        self.servo = servo

    def set_angle(self, angle):
        angle = angle + 45
        multiplicator = angle/90
        write(self.servo, 80 * multiplicator + 115)
        # if angle == -45:
        #     write(self.servo, 115)
        # elif angle == 45:
        #     write(self.servo, 195)
        # else:
        #     write(self.servo, 155)

    def stop(self):
        write(self.servo, 155)
