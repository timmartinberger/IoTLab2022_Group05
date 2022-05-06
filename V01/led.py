import threading
import RPi.GPIO as GPIO
import random
from time import sleep

# Versuch 1.2 - Aufgabe 2 und 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

button_pin = 2
GPIO.setup(button_pin, GPIO.IN)

class LED(threading.Thread):

    def __init__(self, pin, frequency):
        threading.Thread.__init__(self)
        self.pin = pin
        self.frequency = frequency
        self.blinking = False
        self.pwm_signal = GPIO.PWM(self.pin, self.frequency)

    def blink(self):
        self.blinking = True
        self.pwm_signal.start(1)
        while self.blinking:
            if GPIO.input(button_pin):
                random_frequency = random.randint(1,10)
                self.pwm_signal.ChangeFrequency(random_frequency)
            sleep(0.1)

    def run(self):
        self.blink()


def restart_led(led):
    led.blinking = False
    random_frequency = random.randint(1, 10)
    led.frequency = random_frequency
    led.run()


def control_leds():
    led1 = LED(17, 1)
    led2 = LED(18, 1)
    led1.start()
    led2.start()

    while 1:
        button_state = GPIO.input(button_pin)
        if button_state:
            print("button pressed")
        sleep(0.1)

    led1.join()
    led2.join()


def main():
    # Aufgabe 2
    pin = input("Enter the GPIO pin for your led: ")
    freq = input("Enter the desired frequency: ")
    led = LED(pin, freq)
    led.start()
    sleep(5)
    led.blinking = False
    led.join()


if __name__ == "__main__":
    try:
        "Start blinking of LEDs at GPIO pins 17 and 18..."
        control_leds()
    except KeyboardInterrupt:
        "Stopped blinking!"
    finally:
        GPIO.cleanup()
