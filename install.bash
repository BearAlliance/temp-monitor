#!/bin/bash  

sudo apt-get install python
sudo python get-pip.py
sudo pip install RPi.GPIO
sudo pip install python-twitter

echo Don't forget to create apiKeys.txt with your Twitter API info!