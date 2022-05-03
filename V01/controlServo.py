
from gpiozero import Servo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()
servo = Servo(11, min_pulse_width=0.9/1000, max_pulse_width=2.8/1000, pin_factory=factory)

while 1:
  servo.min()
  sleep(2)
  servo.mid()
  sleep(2)
  servo.max()
  sleep(5)

'''



import RPi.GPIO as GPIO
from time import sleep

servoPIN = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 100) # GPIO 11 als PWM mit 100Hz
p.start(2.5) # Initialisierung
try:
  while True:
    p.ChangeDutyCycle(50)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(1)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
'''