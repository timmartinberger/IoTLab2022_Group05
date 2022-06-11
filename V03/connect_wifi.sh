ifconfig wlan0 192.168.0.179 netmask 255.255.255.0 up
iwconfig wlan0 essid off
iwconfig wlan0 essid iot_lab_wlan_bgn_X

echo "\ncheck configuration"
ip route

echo "\ncheck configuration again"
ip route