# coding=utf-8
import RPi.GPIO as GPIO

# Radencoder GPIO pin
encoder_pin = 23

# Als Eingang einrichten
GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_pin, GPIO.IN)


# Counter Methode für die callback Funktion
def count(channel):
    global counter
    counter = counter + 1
    print("Number of impulses" + str(counter))


# Pin 23 generiert ein Interrupt bei fallenden und steigenden Flanken und ruft dabei die Methode count auf
GPIO.add_event_detect(encoder_pin, GPIO.BOTH, callback=count, bouncetime=1)
