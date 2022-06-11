echo "\nchange route for ethernet address space"
ip route del 172.23.0.0/16
ip route add 172.23.0.0/16 dev wlan0 src 192.168.1.1