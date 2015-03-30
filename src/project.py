
import RPi.GPIO as GPIO
import time
import serial

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

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MOTOR_A_1, GPIO.OUT)
	GPIO.setup(MOTOR_A_2, GPIO.OUT)
	GPIO.setup(MOTOR_B_1, GPIO.OUT)
	GPIO.setup(MOTOR_B_2, GPIO.OUT)

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
	port.write(0x1A)
	time.sleep(0.5)

def readGpsAndSendSms():
	print "Reading from GPS"
	rcv = port.read(10)

print "Started"
setupGPIO()
port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, timeout = 3.0)
sendSms("9342833087", "Hai")

while True:
	motorFw()
	time.sleep(5)
	motorBw()
	time.sleep(5)
	motorStop()
	time.sleep(5)
	motorRight()
	time.sleep(5)
	motorLeft()
	time.sleep(5)