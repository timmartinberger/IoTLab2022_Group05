import threading
import RPi.GPIO as GPIO
import random
from time import sleep

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


def main():
    led = LED(17, 1)
    led.start()
    sleep(5)
    led.blinking = False
    led.join()

def restart_led(led):
    led.blinking = False

    random_frequency = random.randint(1, 10)
    led.frequency = random_frequency
    led.run()
    
def control_leds():

    #define the button

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


if __name__ == "__main__":
    try:
        control_leds()
    finally:
        GPIO.cleanup()