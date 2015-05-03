#!/bin/sh
# run_bot.sh
# This will ad to crontab
# @reboot sh /home/pi/pibot/scripts/run_bot.sh > /tmp/pibot_bot_log 2>&1
cd /
cd /home/pi/pibot/src
python bot.py