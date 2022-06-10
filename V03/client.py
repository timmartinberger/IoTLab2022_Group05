import socket
from server import address_families, socket_types
# IP und Port des Servers
IP = '192.168.0.11'
PORT = 8000

# Passenden Address- und Sockettyp w\"ahlen
address_family = address_families[0]
socket_type = socket_types[0]
# Erstellen eines Sockets (TCP und UDP)
sock = socket.socket(address_family, socket_type)
# Verbinden zu einem Server-Socket (Nur TCP)
sock.connect((IP,PORT))
# Sende immer wieder "Hello" an den Server
while True:
    message = "Hello"
    # TCP
    sock.send(message)
    # UDP
    sock.sendto(message, (IP, PORT))