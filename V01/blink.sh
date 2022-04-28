#!/bin/bash
sudo killall -q pigpiod
sudo pigpiod
for((;;))
do
	pigs p 17 255
	sleep 1
	pigs p 17 0
	pigs p 18 255
	sleep 1
	pigs p 18 0
done
