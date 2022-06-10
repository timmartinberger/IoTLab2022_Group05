import socket
from common import address_families, socket_types
# Port des Servers
PORT = 8000
# Lesepuffergr\"o\ss e
BUFFER_SIZE = 1400

# Passenden Address- und Sockettyp w\"ahlen
address_family = address_families[0]
socket_type = socket_types[0]
# Maximale Anzahl der Verbindungen in der Warteschlange
backlog = 1
# Erstellen eines Socket (TCP und UDP)
sock = socket.socket(address_family, socket_type)
sock.bind(('192.168.0.11', PORT))


# Lausche am Socket auf eingehende Verbindungen (Nur TCP)
sock.listen(backlog)
clientsocket, address = sock.accept()
# Daten (der Gr\"o\ss e BUFFER_SIZE) aus dem Socket holen und ausgeben:
while True:
    # TCP:
    data = clientsocket.recv(BUFFER_SIZE)
    print(data)
    # UDP:
    # data, address = sock.recvfrom(BUFFER_SIZE)
    # print(data)