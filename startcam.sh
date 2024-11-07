#!/bin/bash
/usr/local/bin/mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 10 -y" -o "output_http.so -p 8899 -w /usr/local/share/mjpg-streamer/www/"
