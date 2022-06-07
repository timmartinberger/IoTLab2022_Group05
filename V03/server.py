import socket
# Port des Servers
PORT = x
# Lesepuffergr\"o\ss e
BUFFER_SIZE = 1400
# Unterst\"utzte Addresstypen (IPv4, IPv6, lokale Addressen)
address_families = (socket.AF_INET, socket.AF_INET6, socket.AF_UNIX)
# Unterst\"utzte Sockettypen (TCP, UDP, Raw (ohne Typ))
socket_types = (socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW)
# Passenden Address- und Sockettyp w\"ahlen
address_family = address_families[0]
socket_type = socket_types[0]
# Maximale Anzahl der Verbindungen in der Warteschlange
backlog = 1
# Erstellen eines Socket (TCP und UDP)
sock = socket.socket(address_family, socket_type)
sock.bind((’’, PORT))
# Lausche am Socket auf eingehende Verbindungen (Nur TCP)
sock.listen(backlog)
clientsocket, address = sock.accept()
# Daten (der Gr\"o\ss e BUFFER_SIZE) aus dem Socket holen und ausgeben:
while True:
    # TCP:
    data = clientsocket.recv(BUFFER_SIZE)
    print(data)
    # UDP:
    data, address = sock.recvfrom(BUFFER_SIZE)
    print(data)