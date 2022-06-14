import socket
from common import address_families, socket_types
import argparse
import subprocess

# Port des Servers
PORT = 8000
# Lesepuffergr\"o\ss e
BUFFER_SIZE = 1400
DUMMY = False
TCP = True

# Passenden Address- und Sockettyp w\"ahlen
address_family = address_families[0]
socket_type = None
# Maximale Anzahl der Verbindungen in der Warteschlange
backlog = 1
# Erstellen eines Socket (TCP und UDP)
sock = None
clientsocket, address = None, None

def config_protocol(tcp):
    global TCP
    global PORT
    global socket_type
    global sock
    global backlog
    global clientsocket, address
    global address_family

    if tcp:
        TCP = True
        socket_type = socket_types[0]
    else:
        TCP = False
        socket_type = socket_types[1]
    # Konfigurieren des Sockets
    sock = socket.socket(address_family, socket_type)
    sock.bind(('192.168.1.118', PORT))
    # Lausche am Socket auf eingehende Verbindungen (Nur TCP)
    if TCP:
        sock.listen(backlog)
        clientsocket, address = sock.accept()


def start_transmitting():
    if DUMMY:
        # Daten (der Gr\"o\ss e BUFFER_SIZE) aus dem Socket holen und ausgeben:
        while True:
            if TCP:
                data = clientsocket.recv(BUFFER_SIZE)
                print(data)
            else:
                data, address = sock.recvfrom(BUFFER_SIZE)
                print(data)
    else:
        # mplayer starten
        cmd_mplayer = "mplayer -fps 25 -cache 512 - "
        mprocess = subprocess.Popen(cmd_mplayer, shell=True, stdin=subprocess.PIPE)

        while True:
            if TCP:
                data = clientsocket.recv(BUFFER_SIZE)
                mprocess.stdin.write(data)
            else:
                data, address = sock.recvfrom(BUFFER_SIZE)
                mprocess.stdin.write(data)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Stream via UDP or TCP.')
    parser.add_argument('-p', '--protocol', required=True)
    args = vars(parser.parse_args())
    if args['protocol'] == 'udp':
        config_protocol(False)
    elif args['protocol'] == 'tcp':
        config_protocol(True)
    start_transmitting()

