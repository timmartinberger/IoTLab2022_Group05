#!/usr/bin/python
#from requests import options
import math

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import io
import controlCar.servo_ctrl as carControl
import RPi.GPIO as GPIO
import json

import threading
from ikt_car_sensorik import *
#import _servo_ctrl
from math import acos, sqrt, degrees


# Aufgabe 4
#
# Der Tornado Webserver soll die Datei index.html am Port 8081 zur Verfügung stellen
from tornado.options import define, options
define("port", default=8081, help="run on given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


# Aufgabe 3
#
# Der Tornado Webserver muss eine Liste der clients verwalten.  
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    '''Definition der Operationen des WebSocket Servers'''

    def open(self):
        print(f"new connection: {self.request.remote_ip}")
        clients.append(self)

    def on_message(self, message):
        if message == "startParking":
            drivingThread.start()
        elif message == "stopParking":
            drivingThread.stop()
        json_message = {}
        json_message["response"] = message
        json_message = json.dumps(json_message)
        self.write_message(json_message)
        print(f"message received: {message}")

    def on_close(self):
        print("closed connection")
        clients.remove[self]


class DataThread(threading.Thread):
    '''Thread zum Senden der Zustandsdaten an alle Clients aus der Client-Liste'''

    # Aufgabe 3
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, address_ultrasonic_front, address_ultrasonic_back, address_compass, address_infrared, encoder_pin):
        threading.Thread.__init__(self)
        self.stopped = False
        self.setDaemon(True)
        self.set_sensorik(address_ultrasonic_front, address_ultrasonic_back, address_compass, address_infrared, encoder_pin)
        self.start()

    # Aufgabe 3
    #
    # Erstellen Sie hier Instanzen von Klassen aus dem ersten Teilversuch
    def set_sensorik(self, address_ultrasonic_front, address_ultrasonic_back, address_compass, address_infrared, encoder_pin):
        enc = Encoder(encoder_pin)
        self.encoder_thread = EncoderThread(enc)
        self.us_front_thread = UltrasonicThread(address_ultrasonic_front)
        self.us_back_thread = UltrasonicThread(address_ultrasonic_back)
        self.compass_thread = CompassThread(address_compass)
        self.infrared_thread = InfraredThread(address_infrared, self.encoder_thread)

    # Aufgabe 3
    #
    # Hier muessen die Sensorwerte ausgelesen und an alle Clients des Webservers verschickt werden.
    def run(self):
        while not self.stopped:
            json_msg = {}
            json_msg["speed"] = self.encoder_thread.speed
            json_msg["orientation"] = self.compass_thread.bearing
            json_msg["obstcl_front"] = self.us_front_thread.distance
            json_msg["obstcl_back"] = self.us_back_thread.distance
            json_msg["obstcl_side"] = self.infrared_thread.distance
            json_msg["brightness"] = self.us_front_thread.brightness
            json_msg["parking_slot"] = self.infrared_thread.parking_space_length
            json_msg = json.dumps(json_msg)
            for client in clients: 
                client.write_message(json_msg)
            sleep(0.5)


    def stop(self):
        self.stopped = True


class DrivingThread(threading.Thread):
    '''Thread zum Fahren des Autos'''

    max_speed = 3.3

    # Einparken
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self, dataThread):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.dataThread = dataThread
        self.stopped = False
        self.motor = carControl.Motor()
        self.steering = carControl.Steering()
        self.min_ps_length = self.get_parking_slot()

    # Einparken :
    # Definieren Sie einen Thread, der auf die ueber den Webserver erhaltenen Befehle reagiert und den Einparkprozess durchfuehrt
    def run(self):
        print("executing")
        self.motor.set_speed(self.max_speed)
        while not self.stopped:
            
        #    if self.check_ps_exists():
         #       self.motor.stop()
          #      self.continue_forward()
           #     self.go_backward()
            #    self.turn_until_angle_right()
             #   self.turn_until_angle_left()
              #  self.motor.stop()
               # self.steering.set_angle(0)
                #self.stopped = True
            sleep(0.1)

    def check_ps_exists(self):
        ps_length = self.dataThread.infrared_thread.parking_space_length
        return ps_length is not None and ps_length >= self.min_ps_length

    def continue_forward(self):
        distance_continued = 0
        self.motor.set_speed(self.max_speed)
        while distance_continued < 10:
            distance_continued = self.dataThread.encoder_thread.distance - self.dataThread.infrared_thread.last_ps_end
            sleep(0.1)
        self.motor.stop()

    def go_backward(self):
        start_distance = self.dataThread.encoder_thread.distance
        self.motor.set_speed(-self.max_speed)
        distance_travelled = 0
        while distance_travelled < 10:
            distance_travelled = self.dataThread.encoder_thread.distance - start_distance
            sleep(0.1)
        self.motor.stop()

    def turn_until_angle_right(self, angle):
        start_angle = self.dataThread.compass_thread.bearing
        self.steering.set_angle(45)
        self.motor.set_speed(self.max_speed)
        angle_change = 0
        while angle_change < angle:
            angle_change = abs(start_angle - self.dataThread.compass_thread.bearing)
            sleep(0.1)
        self.motor.stop()
    
    def turn_until_angle_left(self, angle):
        start_angle = self.dataThread.compass_thread.bearing
        self.steering.set_angle(-45)
        self.motor.set_speed(self.max_speed)
        angle_change = 0
        while angle_change < angle:
            angle_change = abs(start_angle - self.dataThread.compass_thread.bearing)
            sleep(0.1)
        self.motor.stop()
        
    def get_parking_slot(self):
        # passt schon irgendwie
        w = 19.2
        r = 37.5
        f = 37.5
        b = 7
        alpha = math.acos(1 - (self.dataThread.infrared_thread.distance + w) / (2 * r))
        min_l = math.sqrt(2 * r * w + f**2) + b
        return min_l

    def stop(self):
        print("Stopped driving!")
        self.stopped = True
        self.motor.stop()


if __name__ == "__main__":
    print("Main Thread started")
    # WICHTIG: DataThread und DrivingThread VOR Initialisierung des httpServers starten!
    encoder_pin = 23
    GPIO.setup(encoder_pin, GPIO.IN)
    # The i2c addresses of front and rear ultrasound sensors
    ultrasonic_front_i2c_address = 0x70
    ultrasonic_rear_i2c_address = 0x71
    # The i2c address of the compass sensor
    compass_i2c_address = 0x60
    # The i2c address of the infrared sensor
    infrared_i2c_address = 0x4f

    clients = []
    try:
        dataThread = DataThread(ultrasonic_front_i2c_address, ultrasonic_rear_i2c_address, compass_i2c_address, infrared_i2c_address, encoder_pin)
        drivingThread = DrivingThread(dataThread)

        tornado.options.parse_command_line()
        app = tornado.web.Application(handlers=[(r"/ws", WebSocketHandler), (r"/", IndexHandler), (r'/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(__file__)}),])
        httpServer = tornado.httpserver.HTTPServer(app)
        httpServer.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        print('Program closed!')
        drivingThread.steering.stop()
        drivingThread.motor.stop()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
