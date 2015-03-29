
import RPi.GPIO as GPIO
import time

# Motor Pins
MOTOR_A_1 = 7
MOTOR_A_2 = 8
MOTOR_B_1 = 25
MOTOR_B_2 = 24

# Sensors
FIRE_SENSOR = 23
OBST_SENSOR = 18

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


print "Started"
setupGPIO()

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