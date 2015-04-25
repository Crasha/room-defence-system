#!/bin/bash
cd $(dirname $0)/room-defence-system
ln -s ../pi-facerec-box/negative_eigenface.png .
ln -s ../pi-facerec-box/positive_eigenface.png .
ln -s ../pi-facerec-box/mean.png .
ln -s ../pi-facerec-box/haarcascade_frontalface_alt.xml .
ln -s ../pi-facerec-box/haarcascade_frontalface_alt2.xml .
ln -s ../pi-facerec-box/training.xml .
sudo python Main.py
