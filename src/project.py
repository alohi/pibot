
import RPi.GPIO as GPIO
import time
import serial
import io
import pynmea2

# Motor Pins
MOTOR_A_1 = 7
MOTOR_A_2 = 8
MOTOR_B_1 = 25
MOTOR_B_2 = 24

# Sensors
FIRE_SENSOR = 23
OBST_SENSOR = 18

# Delay for turing in seconds
TURN_DELAY = 3

# Flags
fire_sen_flag = 0
obst_sen_flag = 0

# Num and msg
num = "9342833087"
fireAlert = "fire detected"

gps = ""
gpsRead = False

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MOTOR_A_1, GPIO.OUT)
	GPIO.setup(MOTOR_A_2, GPIO.OUT)
	GPIO.setup(MOTOR_B_1, GPIO.OUT)
	GPIO.setup(MOTOR_B_2, GPIO.OUT)
	GPIO.setup(FIRE_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(OBST_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def motorFw():
	print "Motor Forward"
	GPIO.output(MOTOR_A_1, True)
	GPIO.output(MOTOR_A_2, False)
	GPIO.output(MOTOR_B_1, True)
	GPIO.output(MOTOR_B_2, False)

def motorBw():
	print "Motor Backward"
	GPIO.output(MOTOR_A_1, False)
	GPIO.output(MOTOR_A_2, True)
	GPIO.output(MOTOR_B_1, False)
	GPIO.output(MOTOR_B_2, True)

def motorRight():
	print "Motor Right"
	GPIO.output(MOTOR_A_1, False)
	GPIO.output(MOTOR_A_2, False)
	GPIO.output(MOTOR_B_1, False)
	GPIO.output(MOTOR_B_2, True)
	time.sleep(TURN_DELAY)
	GPIO.output(MOTOR_B_1, False)
	GPIO.output(MOTOR_B_2, False)

def motorLeft():
	print "Motor Left"
	GPIO.output(MOTOR_A_1, False)
	GPIO.output(MOTOR_A_2, True)
	GPIO.output(MOTOR_B_1, False)
	GPIO.output(MOTOR_B_2, False)
	time.sleep(TURN_DELAY)
	GPIO.output(MOTOR_A_1, False)
	GPIO.output(MOTOR_A_2, False)

def motorStop():
	print "Motor Backward"
	GPIO.output(MOTOR_A_1, False)
	GPIO.output(MOTOR_A_2, False)
	GPIO.output(MOTOR_B_1, False)
	GPIO.output(MOTOR_B_2, False)

def sendSms(num, msg):
	print "SMS is sending."
	port.write("AT+CMGF=1\r\n")
	time.sleep(0.5)
	port.write("AT+CMGS=\"" + num + "\"\r\n")
	time.sleep(0.5)
	port.write(msg + "\r\n")
	sub = "1A"
	port.write(sub.decode("hex"))
	time.sleep(0.5)

def readGps():
	msg = ""
	try:
		#rcv = port.read(30)
		#port.flushInput()
		#print rcv
		#time.sleep(0.2)
		rcv = port.readline()
		print rcv
		msg = rcv.split(',')
		print msg
		port.flushInput()
		if msg[0] == "$GPGGA":
			try:
				gps = pynmea2.parse(rcv)
				gpsRead = True
				print "Time " + str(gps.timestamp)
				print "Lat " + gps.lat		
			except pynmea2.ParseError:
				print "Parse error"	
	except serial.SerialException:
		print "Serial error"
		#port.flushInput()

def readObstSen():
	if GPIO.input(OBST_SENSOR) == 0:
		time.sleep(0.3)
		return 1
	else:
		return 0

def readFireSen():
	if GPIO.input(FIRE_SENSOR) == 0:
		time.sleep(0.3)
		return 1
	else:
		return 0

print "Started"
setupGPIO()
port = serial.Serial("/dev/ttyAMA0", baudrate = 9600, timeout = 3.0)

while True:
	#motorFw()
	#time.sleep(5)
	#motorBw()
	#time.sleep(5)
	#motorStop()
	#time.sleep(5)
	#motorRight()
	#time.sleep(5)
	#motorLeft()
	#time.sleep(5)
	fire_val = readFireSen()
	obst_val = readObstSen()
	#readGps()

	# Fire sensor part
	if fire_val == 1:
		print "Fire detected"
		if fire_sen_flag == 0:
			print "flag is 0"
			fire_sen_flag = 1
			motorStop()
			sendSms(num, fireAlert)

	else:
		fire_sen_flag = 0

	# Obstacle part
	if obst_val == 1:
		print "Obstacle"
		readGps()
		if gpsRead == True:
			print gps.timestamp
	#time.sleep(2)
