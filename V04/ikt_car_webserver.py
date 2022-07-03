#!/usr/bin/python
#from requests import options
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import io
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
    def __init__(self):#, address_ultrasonic_front, address_ultrasonic_back, address_compass, address_infrared, encoder_pin):
        threading.Thread.__init__(self)
        self.stopped = False
        self.setDaemon(True)
        #self.set_sensorik(address_ultrasonic_front, address_ultrasonic_back, address_compass, address_infrared, encoder_pin)
        self.start()


    # Aufgabe 3
    #
    # Erstellen Sie hier Instanzen von Klassen aus dem ersten Teilversuch
    def set_sensorik(self, address_ultrasonic_front, address_ultrasonic_back, address_compass, address_infrared, encoder_pin):
        encoder = Encoder(encoder_pin)
        self.encoder_thread = EncoderThread(encoder)
        self.us_front_thread = UltrasonicThread(address_ultrasonic_front)
        self.us_back_thread = UltrasonicThread(address_ultrasonic_back)
        self.compass_thread = CompassThread(address_compass)
        self.infrared_thread = InfraredThread(address_infrared, encoder_thread)

    # Aufgabe 3
    #
    # Hier muessen die Sensorwerte ausgelesen und an alle Clients des Webservers verschickt werden.
    def run(self):
        while not self.stopped:
            json_msg = {}
            # Todo: Change values to thread call
            json_msg["distance"] = 25
            json_msg["speed"] = 40
            json_msg["orientation"] = 225
            json_msg["obstcl_front"] = 4
            json_msg["obstcl_back"] = 99
            json_msg["obstcl_side"] = 119
            json_msg["brightness"] = 71
            json_msg["parking_slot"] = 8
            json_msg = json.dumps(json_msg)
            for client in clients: 
                client.write_message(json_msg)
            sleep(0.5)


    def stop(self):
        self.stopped = True


class DrivingThread(threading.Thread):
    '''Thread zum Fahren des Autos'''

    # Einparken
    #
    # Hier muss der Thread initialisiert werden.
    def __init__(self):
        return 0

    # Einparken
    #
    # Definieren Sie einen Thread, der auf die ueber den Webserver erhaltenen Befehle reagiert und den Einparkprozess durchfuehrt
    def run(self):
        while not self.stopped:
            continue

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    print("Main Thread started")
    # WICHTIG: DataThread und DrivingThread VOR Initialisierung des httpServers starten!
    clients = []
    dataThread = DataThread()


    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/ws", WebSocketHandler), (r"/", IndexHandler), (r'/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(__file__)}),])
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# Aufgabe 3
#
# Erstellen und starten Sie hier eine Instanz des DataThread und starten Sie den Webserver.

# Einparken
#
# Erstellen und starten Sie hier eine Instanz des DrivingThread, um das Einparken zu ermoeglichen.
