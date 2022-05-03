#! /bin/bash
# Versuch 1.1 - Aufgabe 6

echo "Reading state of button at GPIO pin 2..."

for ((;;))
do
	state=$(pigs r 2)
	sleep 0.2
	echo "state = ${state}"
done
