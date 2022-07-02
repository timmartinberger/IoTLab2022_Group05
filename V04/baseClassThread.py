import threading
from time import sleep
from ikt_car_sensorik import Ultrasonic


class UltrasonicThread(threading.Thread):
    stop = False
    light = -1.0
    range = -1.0

    def __init__(self, address):
        threading.Thread.__init__(self)
        sleep(0.1)
        self.ultrasonic = Ultrasonic(address)
        self.setDaemon(True)
        self.start()

    def run(self):
        while not self.stop:
            pass

    def stop(self):
        self.stop = True
