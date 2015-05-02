
import RPi.GPIO as GPIO
import time
import serial
import io
import pynmea2

# Motor Pins
MOTOR_A_1 		= 7
MOTOR_A_2 		= 8
MOTOR_B_1 		= 25
MOTOR_B_2 		= 24

# Sensors
FIRE_SENSOR 	= 23
OBST_SENSORL 	= 18
OBST_SENSORR 	= 11
LOAD_OUTPUT		= 9

# Delay for turing in seconds
TURN_DELAY 		= 3

# Flags
fire_sen_flag 	= 0
obst_sen_flag 	= 0

# Num and msg
num 			= "9342833087"
fireAlert 		= "fire detected"

gps 			= ""
gpsReadFlag 	= False

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MOTOR_A_1, GPIO.OUT)									# Output
	GPIO.setup(MOTOR_A_2, GPIO.OUT)							
	GPIO.setup(MOTOR_B_1, GPIO.OUT)
	GPIO.setup(MOTOR_B_2, GPIO.OUT)
	GPIO.setup(LOAD_OUTPUT, GPIO.OUT)
	GPIO.setup(FIRE_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(OBST_SENSORL, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(OBST_SENSORR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

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
		rcv = port.readline()
		#print rcv
		msg = rcv.split(',')
		#print msg
		#port.flushInput()
		if msg[0] == "$GPGGA":
			try:
				global gps
				gps = pynmea2.parse(rcv)
				global gpsReadFlag
				gpsReadFlag = True
				print str(gpsReadFlag)
				print "Time " + str(gps.timestamp)
				print "Lat " + gps.lat		
			except pynmea2.ParseError:
				print "Parse error"	
	except serial.SerialException:
		print "Serial error"

def readObstSenL():
	if GPIO.input(OBST_SENSORL) == 0:
		time.sleep(0.3)
		return 1
	else:
		return 0

def readObstSenR():
	if GPIO.input(OBST_SENSORR) == 0:
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
port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 3.0)

GPIO.output(LOAD_OUTPUT, False)

gpsReadFlag = False
motorFw()

while True:
	motorFw()
	
	# read sensors
	fire_val  = readFireSen()
	obst_vall = readObstSenL()
	obst_valr = readObstSenR()

	# Fire sensor part
	if fire_val == 1:
		print "Fire detected"
		print str(gpsReadFlag)
		if fire_sen_flag == 0:
			print "flag is 0"
			fire_sen_flag = 1
			motorStop()
			GPIO.output(LOAD_OUTPUT, True)
			print str(gpsReadFlag)
			if gpsReadFlag == True:
				gpsReadFlag = False
				print "GPS Data found"
				#sms = "Fire detected at \n" + "Lat: " + str(gps.lat) + "\n" + "Lon: " + str(gps.lon) + "\n" + "LatDir: " + str(gps.lat_dir) + "\n" + "LonDir: " + str(gps.lon_dir) + "\n" + "qua: " + str(gps.gps_qual) + "\n" + "Sat: " + str(gps.num_sats) + "\n" + "Alt: " + str(gps.altitude) + "\n" +  
				sms = str(gps.timestamp) + ": " + str(gps.latitude)  + str(gps.latitude_minutes) + str(gps.latitude_seconds)
				print sms
				sendSms(num, fireAlert)
			else:
				print "GPS Data Not Found"

	elif fire_val == 0:
		GPIO.output(LOAD_OUTPUT, False)

	else:
		if fire_sen_flag == 1:
			motorFw()
			fire_sen_flag = 0

	# Obstacle part
	if obst_vall == 1:
		motorRight()
	elif obst_valr == 1:
		motorLeft()

	# read gps
	readGps()
