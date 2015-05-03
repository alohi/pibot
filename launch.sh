#!/bin/sh
# launch.sh
# This will ad to crontab
# @reboot sh /home/pi/pibot/launch.sh > /tmp/pibot_log 2>&1
cd /
cd /home/pi/pibot/src
python cam.py
#sudo python bot.py
cd /
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental
LD_LIBRARY_PATH=/usr/local/lib ./mjpg_streamer -i "input_file.so -f 15 -r 1280x720 -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"