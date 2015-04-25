#!/bin/bash
echo 0 > /sys/class/gpio/gpio4/value
echo 0 > /sys/class/gpio/gpio17/value
echo 0 > /sys/class/gpio/gpio22/value
echo 0 > /sys/class/gpio/gpio23/value
echo 0 > /sys/class/gpio/gpio27/value


echo 4 > /sys/class/gpio/unexport
echo 17 > /sys/class/gpio/unexport
echo 22 > /sys/class/gpio/unexport
echo 23  > /sys/class/gpio/unexport
echo 27 > /sys/class/gpio/unexport

