import socket
# Unterst\"utzte Addresstypen (IPv4, IPv6, lokale Addressen)
address_families = (socket.AF_INET, socket.AF_INET6, socket.AF_UNIX)
# Unterst\"utzte Sockettypen (TCP, UDP, Raw (ohne Typ))
socket_types = (socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW)