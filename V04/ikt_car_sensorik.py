#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from time import time, sleep
import threading
import sys
from turtle import speed
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
        range_High_Byte = bus.read_byte_data(self.address, 0x02)  # höherwertiges Byte
        range_Low_Byte = bus.read_byte_data(self.address, 0x03)  # niederwertiges Byte

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
        threading.Thread.__init__(self)
        self.us = Ultrasonic(address)
        self.stopped = False
        self.setDaemon(True)
        self.start()

    # Aufgabe 4
    #
    # Schreiben Sie die Messwerte in die lokalen Variablen
    def run(self):
        while not self.stopped:
            self.brightness = self.us.get_brightness()
            self.distance = self.us.get_distance()
            sleep(0.1)

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
        threading.Thread.__init__(self)
        self.compass = Compass(address)
        self.stopped = False
        self.setDaemon(True)
        self.start()

    # Aufgabe 4
    #
    # Diese Methode soll den Kompasswert aktuell halten.
    def run(self):
        while not self.stopped:
            self.bearing = self.compass.get_bearing()
            sleep(0.1)

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
        distance_IR_voltage = bus.read_byte(self.address)
        return distance_IR_voltage

    # Aufgabe 3
    #
    # Der Spannungswert soll in einen Distanzwert umgerechnet werden.
    def get_distance(self):
        '''
        Der Wertebereich der Spannung liegt zwischen 0x00 (0 Volt) und 0xFF (5 Volt).
        Der Spannungswert entspricht Distanzen zwischen 10cm und 80cm.
        '''
        voltage = int.from_bytes(self.get_voltage(), "big")
        voltage = 10 + (voltage / 255) * 70



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
        threading.Thread.__init__(self)
        self.infrared = Infrared(address)
        self.encoder = encoder
        self.stopped = False
        self.setDaemon(True)
        self.start()

    def run(self):
        while not self.stopped:
            self.read_infrared_value()
            self.calculate_parking_space_length()
            sleep(0.1)

    # Aufgabe 4
    #
    # Diese Methode soll den Infrarotwert aktuell halten
    def read_infrared_value(self):
        self.distance = self.infrared.get_distance()

    # Aufgabe 5
    # ToDo
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
    count = 32.0

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
    def count(self, channel):
        self.steps_travelled += 1

    # Aufgabe 2
    #
    # Diese Methode soll die gesamte zurueckgelegte Distanz zurueckgeben.
    def get_travelled_dist(self):
        return self.steps_travelled * self.STEP_LENGTH


class EncoderThread(threading.Thread):
    ''' Thread-class for holding speed and distance data of all encoders'''

    # current speed in m/s.
    speed = 0

    # currently traversed distance.
    distance = 0

    # Aufgabe 4
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, encoder):
        threading.Thread.__init__(self)
        self.encoder = encoder
        self.stopped = False
        self.setDaemon(True)
        self.start()

    def run(self):
        while not self.stopped:
            self.get_values()
            sleep(0.1)

    # Aufgabe 4
    # 
    # Diese Methode soll die aktuelle Geschwindigkeit sowie die zurueckgelegte Distanz aktuell halten.
    def get_values(self):
        prev_distance = self.distance
        self.distance = self.encoder.get_travelled_dist()
        speed = (self.distance - prev_distance) / 0.1

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
    # ToDo: Tragen Sie die i2c Adressen der Sensoren hier ein

    # The i2c addresses of front and rear ultrasound sensors
    ultrasonic_front_i2c_address = 0x00;
    ultrasonic_rear_i2c_address = 0x00;

    # The i2c address of the compass sensor
    compass_i2c_address = 0x00

    # The i2c address of the infrared sensor
    infrared_i2c_address = 0x00

# Aufgabe 6
# Hier sollen saemtlichen Messwerte periodisch auf der Konsole ausgegeben werden.
    # Threads erstellen
    encoder = Encoder(encoder_pin)
    encoder_thread = EncoderThread(encoder)
    us_front_thread = UltrasonicThread(ultrasonic_front_i2c_address)
    us_rear_thread = UltrasonicThread(ultrasonic_rear_i2c_address)
    compass_thread = CompassThread(compass_i2c_address)
    infrared_thread = InfraredThread(infrared_i2c_address, encoder_thread)

    try:
        prev_dist = 0
        t = 0
        while(1):
            dist = encoder_thread.distance
            car_speed = encoder_thread.speed
            direction = compass_thread.bearing
            obstacle_front = us_front_thread.distance
            obstacle_back = us_rear_thread.distance
            obstacle_side = infrared_thread.distance
            brightness_front = us_front_thread.brightness
            parking_slot = infrared_thread.parking_space_length
            print(f"Status t={t}:\n\
            zurückgelegte Strecke: {dist}m\n\
            Geschwindigkeit: {car_speed}m/s\n\
            Ausrichtung: {direction}\n\
            Distanz bis Hindernis vorne: {obstacle_front}m\n\
            Distanz bis Hindernis hinten: {obstacle_back}m\n\
            Distanz bis Hindernis seitlich: {obstacle_side}m\n\
            Helligkeit vorne: {brightness_front}\n\
            Länge der Parklücke: {parking_slot}m\n\n")
            sleep(1)
            t += 1 
    except KeyboardInterrupt:
        print('Program closed!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)