#!/bin/sh
# run_stream.sh
# This will ad to crontab
# @reboot sh /home/pi/pibot/scripts/run_stream.sh > /tmp/pibot_stream_log 2>&1
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental
LD_LIBRARY_PATH=/usr/local/lib ./mjpg_streamer -i "input_file.so -f 15 -r 1280x720 -f /tmp -n pic.jpg" -o "output_http.so -w /usr/local/www"