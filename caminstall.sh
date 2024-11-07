#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install cmake -y
sudo apt-get install cmake libjpeg62-turbo-dev
wget https://osoyoo.com/driver/picar/master.zip
unzip master.zip
cd mjp*g-*
cd mjpg-*
make
sudo make install
cd $home


