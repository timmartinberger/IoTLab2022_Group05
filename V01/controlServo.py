
from gpiozero import Servo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO

# Versuch 1.2 - Aufgabe 4
# Unabhängig von der Aufgabe:
# Dies ist ein Versuch die Servos mittels Python zu steuern.

factory = PiGPIOFactory()
servo = Servo(11, min_pulse_width=0.7/1000, max_pulse_width=2.8/1000, pin_factory=factory)
try:
  while 1:
    servo.min()
    sleep(2)
    servo.mid()
    sleep(2)
    servo.max()
    sleep(5)
except KeyboardInterrupt:
  servo.value = None
  print("\nAbort servo control!\n")

'''
# Evquivalent code (not working yet)
servoPIN = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 11 als PWM mit 100Hz
p.start(50) # Initialisierung
try:
  while True:
    p.ChangeDutyCycle(5)
    sleep(2)
    p.ChangeDutyCycle(7.5)
    p.ChangeDutyCycle(0)
    sleep(2)
    p.ChangeDutyCycle(12)
    p.ChangeDutyCycle(0)
    sleep(5)
except KeyboardInterrupt:
  print("\nAbort servo control!\n")
  p.stop()
  GPIO.cleanup()
'''
