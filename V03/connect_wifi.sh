ifconfig wlan0 192.168.1.xxx netmask 255.255.255.0 up
iwconfig wlan0 essid off
iwconfig wlan0 essid iot_lab_wlan_bgn_X

echo "check configuration"
ip route

echo "change route for ethernet address space"
ip route del 172.23.0.0/16
ip route add 172.23.0.0/16 dev wlan0 src 192.168.1.1

echo "check configuration again"
ip route