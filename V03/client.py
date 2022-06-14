from pickle import TRUE
import socket
import argparse
from time import sleep
from common import address_families, socket_types
import subprocess

# IP und Port des Servers
IP = '192.168.1.118'
PORT = 8000
BUFFER_SIZE = 1400
DUMMY = False
TCP = True

# Passenden Address- und Sockettyp w\"ahlen
address_family = address_families[0]
socket_type = None
# Erstellen eines Sockets (TCP und UDP)
sock = None

def config_protocol(tcp):
    global TCP
    global socket_type
    global sock

    if tcp:
        TCP = True
        socket_type = socket_types[0]
    else:
        TCP = False
        socket_type = socket_types[1]
    # Konfigurieren des Sockets
    sock = socket.socket(address_family, socket_type)
    # Verbinden zu einem Server-Socket
    sock.connect((IP, PORT))



def start_transmitting(time, fps, width, height, bitrate):
    # Sende immer wieder "Hello" an den Server
    if DUMMY:
        while True:
            message = b"Hello\n"
            if TCP:
                sock.send(message)
            else:
                sock.sendto(message, (IP, PORT))
                sleep(1)
    else:
        # actual video streaming
        # cmd_raspivid = f"raspivid -t {time} -fps {fps} -w {width} -h {height} -b {bitrate} -o - "
        cmd_raspivid = "raspivid -t 0 -fps 20 -w 1280 -h 720 -b 2000000 -o - "
        rasprocess = subprocess.Popen(cmd_raspivid, shell=True, stdout=subprocess.PIPE)
        while True:
            data = rasprocess.stdout.read(BUFFER_SIZE)
            if TCP:
                sock.send(data)
            else:
                sock.sendto(data, (IP, PORT))


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Stream via UDP or TCP.')
    parser.add_argument('-p', '--protocol', required=True)
    parser.add_argument('-t', '--time')
    parser.add_argument('-f', '--fps')
    parser.add_argument('-b', '--bitrate')
    parser.add_argument('-w', '--width')
    parser.add_argument('-he', '--height')
    args = vars(parser.parse_args())
    if args['protocol'] == 'udp':
        config_protocol(False)
    elif args['protocol'] == 'tcp':
        config_protocol(True)
        pass

    time = 0
    fps = 20
    width = 1280
    height = 720
    bitrate = 2000000
    if args['time'] is not None:
        time = args['time']
    if args['fps'] is not None:
        fps = args['fps']
    if args['width'] is not None:
        width = args['width']
    if args['height'] is not None:
        height = args['height']
    if args['bitrate'] is not None:
        bitrate = args['bitrate']
    start_transmitting(time, fps, width, height, bitrate)
