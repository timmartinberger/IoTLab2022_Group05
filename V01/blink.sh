#!/bin/bash
# Versuch 1.1 - Aufgabe 5

if [[ ! $(ps -ef | grep -v grep | grep pigpiod) ]]; then
	sudo systemctl start pigpiod
	echo "Starting pigpiod deamon..."
else
	echo "Pigpiod deamon is running. Start blinking..."
fi

for((;;))
do
	pigs p 17 255
	sleep 1
	pigs p 17 0
	pigs p 18 255
	sleep 1
	pigs p 18 0
done

