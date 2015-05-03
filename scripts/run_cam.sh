#!/bin/sh
# run_cam.sh
# This will ad to crontab
# @reboot sh /home/pi/pibot/scripts/run_cam.sh > /tmp/pibot_cam_log 2>&1
cd /
cd /home/pi/pibot/src
python cam.py