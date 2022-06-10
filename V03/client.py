from pickle import TRUE
import socket
from time import sleep
from common import address_families, socket_types
import subprocess

# IP und Port des Servers
IP = '192.168.0.11'
PORT = 8000
BUFFER_SIZE = 1400
DUMMY = True
TCP = True
UDP = not TCP

# Passenden Address- und Sockettyp w\"ahlen
address_family = address_families[0]
socket_type = socket_types[0]
# Erstellen eines Sockets (TCP und UDP)
sock = socket.socket(address_family, socket_type)
# Verbinden zu einem Server-Socket (Nur TCP)
sock.connect((IP,PORT))


# Sende immer wieder "Hello" an den Server
if DUMMY:
    while True:
        message = b"Hello\n"
        if TCP:
            sock.send(message)
        elif UDP:
            sock.sendto(message, (IP, PORT))
            sleep(1)
else:
    # tatsächliches video streaming
    time = 0
    fps = 20
    bitrate = 2000000
    cmd_raspivid = f'raspivid -t {time} -fps {fps} -w 1280 -h 720 -b {bitrate} -o -'
    rasprocess = subprocess.Popen(cmd_raspivid,shell=True,stdout=subprocess.PIPE)
    while True:
        data = rasprocess.stdout.read(BUFFER_SIZE)
        if TCP:
            sock.send(data)
        elif UDP:
            sock.sendto(data, (IP, PORT))