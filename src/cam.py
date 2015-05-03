import os
import time
import sys

os.mkdir("/tmp/stream")
while True:
	print 'capturing frame'
	os.system("fswebcam -d /dev/video0 -r 1280x720 /tmp/pic.jpg")
	print "captured"
	time.sleep(2)
