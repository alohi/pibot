
import RPi.GPIO as GPIO
import time
import serial
import io
import pynmea2

serialEnable = True

# Motor Pins
MOTOR_A_1 		= 8
MOTOR_A_2 		= 7
MOTOR_B_1 		= 24
MOTOR_B_2 		= 25

# Sensors
FIRE_SENSOR 	= 11
OBST_SENSORL 	= 18
OBST_SENSORR 	= 23
LOAD_OUTPUT		= 9

# Delay for turing in seconds
TURN_DELAY 		= 3

# Flags
fire_sen_flag 	= 0
obst_sen_flag 	= 0

# Num and msg
num 			= "9740613430"
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
	GPIO.setup(FIRE_SENSOR, GPIO.IN)
	GPIO.setup(OBST_SENSORL, GPIO.IN)
	GPIO.setup(OBST_SENSORR, GPIO.IN)

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
	print "Motor Stop"
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
		msg = rcv.split(',')
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

print "Started"
setupGPIO()
#if serialEnable == True:
port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 3.0)

# Switch of load initially
GPIO.output(LOAD_OUTPUT, False)

gpsReadFlag = False

_flag = False

motorFw()

while True:
	#motorFw()

	# Fire sensor part
	if GPIO.input(FIRE_SENSOR) == 1:
		time.sleep(0.3)
		motorStop()
		print "Fire detected"
		print str(gpsReadFlag)
		if fire_sen_flag == 0:
			#motorStop()
			print "flag is 0"
			fire_sen_flag = 1
			#motorStop()
			GPIO.output(LOAD_OUTPUT, True)
			print str(gpsReadFlag)
			if gpsReadFlag == True:
				gpsReadFlag = False
				print "GPS Data found"  
				sms = "fire detected \n" + str(gps.timestamp) + ": " + str(gps.latitude)  + str(gps.latitude_minutes) + str(gps.latitude_seconds)
				print sms
				sendSms(num, sms)
			else:
				print "GPS Data Not Found"

	else:
		time.sleep(0.3)
		motorFw()
		GPIO.output(LOAD_OUTPUT, False)
		fire_sen_flag = 0	
	if GPIO.input(OBST_SENSORL) == 1 and GPIO.input(OBST_SENSORR) == 1:
		time.sleep(0.3)
		if _flag == False:
			_flag = True
			motorRight()
			motorFw()
		elif _flag == True:
			_flag = False
			motorLeft()
			motorFw()	
	elif GPIO.input(OBST_SENSORL) == 1:
		time.sleep(0.3)
		motorRight()
		motorFw()
	elif  GPIO.input(OBST_SENSORR) == 1:
		time.sleep(0.3)
		motorLeft()
		motorFw()

	# read gps
	#if serialEnable == True:
	readGps()
