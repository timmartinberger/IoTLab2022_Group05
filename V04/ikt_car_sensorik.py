#!/usr/bin/python
import os
from time import time, sleep
import threading
import RPi.GPIO as GPIO
import smbus
import math

GPIO.setmode(GPIO.BCM)

# 1 indicates /dev/i2c-1 (port I2C1)
bus = smbus.SMBus(1)

def combine_high_low(high, low):
    return (high << 8) | low


#################################################################################
# Sensors
#################################################################################

#################################################################################
# Ultrasonic
#################################################################################

class Ultrasonic():
    '''This class is responsible for handling i2c requests to an ultrasonic sensor'''

    def __init__(self, address):
        self.address = address

    # Aufgabe 2
    #
    # Diese Methode soll ein Datenbyte an den Ultraschallsensor senden um eine Messung zu starten
    def write(self, value):
        bus.write_byte_data(self.address, 0x00, 0x51)
        sleep(0.07)

    # Aufgabe 2
    #
    # Diese Methode soll den Lichtwert auslesen und zurueckgeben.
    def get_brightness(self):
        light_v = bus.read_byte_data(self.address, 0x01)
        return light_v

    # Aufgabe 2
    #
    # Diese Methode soll die Entfernung auslesen und zurueckgeben.
    def get_distance(self):
        range_High_Byte = bus.read_byte_data(address_SRF_v, 0x02)  # höherwertiges Byte
        range_Low_Byte = bus.read_byte_data(address_SRF_v, 0x03)  # niederwertiges Byte

        return combine_high_low(range_High_Byte, range_Low_Byte)


    def get_address(self):
        return self.address


class UltrasonicThread(threading.Thread):
    ''' Thread-class for holding ultrasonic data '''

    # distance to obstacle in cm
    distance = 0

    # brightness value
    brightness = 0

    # Aufgabe 4
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, address):
        return 0

    # Aufgabe 4
    #
    # Schreiben Sie die Messwerte in die lokalen Variablen
    def run(self):
        while not self.stopped:
            continue

    def stop(self):
        self.stopped = True


#################################################################################
# Compass
#################################################################################

class Compass(object):
    '''This class is responsible for handling i2c requests to a compass sensor'''

    def __init__(self, address):
        self.address = address

    # Aufgabe 2
    #
    # Diese Methode soll den Kompasswert auslesen und zurueckgeben.
    def get_bearing(self):
        bear_High_Byte = bus.read_byte_data(self.address, 2)  # höherwertiges Byte
        bear_Low_Byte = bus.read_byte_data(self.address, 3)  # niederwertiges Byte

        return combine_high_low(bear_High_Byte, bear_Low_Byte)


class CompassThread(threading.Thread):
    ''' Thread-class for holding compass data '''

    # Compass bearing value
    bearing = 0

    # Aufgabe 4
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, address):
        return 0

    # Aufgabe 4
    #
    # Diese Methode soll den Kompasswert aktuell halten.
    def run(self):
        while not self.stopped:
            continue

    def stop(self):
        self.stopped = True


#################################################################################
# Infrared
#################################################################################

class Infrared(object):
    '''This class is responsible for handling i2c requests to an infrared sensor'''

    def __init__(self, address):
        self.address = address

    # Aufgabe 2
    #
    # In dieser Methode soll der gemessene Spannungswert des Infrarotsensors ausgelesen werden.
    def get_voltage(self):
        distance_IR_voltage = bus.read_byte(address_IR)
        return distance_IR_voltage

    # Aufgabe 3
    #
    # Der Spannungswert soll in einen Distanzwert umgerechnet werden.
    def get_distance(self):
        return 0


class InfraredThread(threading.Thread):
    ''' Thread-class for holding Infrared data '''

    # distance to an obstacle in cm
    distance = 0

    # length of parking space in cm
    parking_space_length = 0

    # Aufgabe 4
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, address, encoder=None):
        return 0

    def run(self):
        while not self.stopped:
            read_infrared_value()
            calculate_parking_space_length()

    # Aufgabe 4
    #
    # Diese Methode soll den Infrarotwert aktuell halten
    def read_infrared_value(self):
        return 0

    # Aufgabe 5
    #
    # Hier soll die Berechnung der Laenge der Parkluecke definiert werden
    def calculate_parking_space_length(self):
        return 0

    def stop(self):
        self.stopped = True


#################################################################################
# Encoder
#################################################################################

class Encoder(object):
    ''' This class is responsible for handling encoder data '''

    # number of encoder steps
    count = 16.0

    # Aufgabe 2
    #
    # Wieviel cm betraegt ein einzelner Encoder-Schritt?
    STEP_LENGTH = math.pi * 5 / count  # in cm


    def __init__(self, pin):
        self.pin = pin
        self.steps_travelled = 0
        GPIO.add_event_detect(encoder_pin, GPIO.BOTH, callback=self.count, bouncetime=1)


    # Aufgabe 2
    #
    # Jeder Flankenwechsel muss zur Berechnung der Entfernung gezaehlt werden.
    # Definieren Sie alle dazu noetigen Methoden.
    def count(channel):
        self.steps_travelled += 1

    # Aufgabe 2
    #
    # Diese Methode soll die gesamte zurueckgelegte Distanz zurueckgeben.
    def get_travelled_dist(self):
        return self.steps_travelled * STEP_LENGTH


class EncoderThread(threading.Thread):
    ''' Thread-class for holding speed and distance data of all encoders'''

    # current speed.
    speed = 0

    # currently traversed distance.
    distance = 0

    # Aufgabe 4
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, encoder):
        return 0

    def run(self):
        while not self.stopped:
            get_values()

    # Aufgabe 4
    #
    # Diese Methode soll die aktuelle Geschwindigkeit sowie die zurueckgelegte Distanz aktuell halten.
    def get_values(self):
        return 0

    def stop(self):
        self.stopped = True


#################################################################################
# Main Thread
#################################################################################	

if __name__ == "__main__":
    # The GPIO pin to which the encoder is connected
    encoder_pin = 23
    GPIO.setup(encoder_pin, GPIO.IN)

    # Aufgabe 1
    #
    # Tragen Sie die i2c Adressen der Sensoren hier ein

    # The i2c addresses of front and rear ultrasound sensors
    ultrasonic_front_i2c_address = 0x00;
    ultrasonic_rear_i2c_address = 0x00;

    # The i2c address of the compass sensor
    compass_i2c_address = 0x00

    # The i2c address of the infrared sensor
    infrared_i2c_address = 0x00

# Aufgabe 6
#
# Hier sollen saemtlichen Messwerte periodisch auf der Konsole ausgegeben werden.
