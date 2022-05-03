import RPi.GPIO as GPIO
from time import sleep
import sys
import os

GPIO.setmode(GPIO.BCM)

def blink():
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    while 1:
        GPIO.output(17, 1)
        sleep(0.5)
        GPIO.output(17, 0)
        GPIO.output(18, 1)
        sleep(0.5)
        GPIO.output(18, 0)


if __name__ == "__main__":
    try:
        blink()

    # How to handle keyboard interrupt:
    # https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
    except KeyboardInterrupt:
        print("Program closed")
        GPIO.cleanup()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
