import time
import SocketServer
import threading
import pygame
from threading import Thread

import Constants as CONSTANTS
import MotorModes as MOTOR_MODES

from Motor import Motor
from MotorHandler import MotorHandler
from Sensor import Sensor
from SensorHandler import SensorHandler
from RobotState import RobotState
from SerialHandler import SerialHandler
from NetworkHandler import NetworkHandler
from MessageQueue import MessageQueue
from JoystickReader import JoystickReader

from time import gmtime, strftime

def runServer(server):
	server.serve_forever()

def motorCommunicationThread():
	while True:
		inboundMotorMessage = motorSerialHandler.getMessage()
		motorHandler.updateMotors(inboundMotorMessage)
		outboundMotorMessage = motorHandler.getMotorStateMessage()
		motorSerialHandler.sendMessage(outboundMotorMessage)
	
def sensorCommunicationThread():
	while True:
		inboundSensorMessage = sensorSerialHandler.getMessage()
		sensorHandler.updateSensors(inboundSensorMessage)
		sensorHandler.printSensorValues()

#initialize handlers
motorHandler = MotorHandler()
sensorHandler = SensorHandler()

if CONSTANTS.USING_MOTOR_BOARD:
	motorSerialHandler = SerialHandler('COM8')
	motorSerialHandler.initSerial()
	
if CONSTANTS.USING_SENSOR_BOARD:
	sensorSerialHandler = SerialHandler('COM3')
	sensorSerialHandler.initSerial()

#initialize network comms & server thread
if CONSTANTS.USING_NETWORK_COMM:
	inboundMessageQueue = MessageQueue()
	outboundMessageQueue = MessageQueue()

	networkHandler = NetworkHandler(inboundMessageQueue, outboundMessageQueue)

	server = SocketServer.TCPServer((CONSTANTS.HOST, CONSTANTS.PORT), networkHandler)
	serverThread = Thread(target=runServer, args=(server,))
	serverThread.start()




# initialize motors
leftDriveMotor       = Motor("LeftDriveMotor",       CONSTANTS.LEFT_DRIVE_DEVICE_ID,       MOTOR_MODES.K_PERCENT_VBUS)
rightDriveMotor      = Motor("RightDriveMotor",      CONSTANTS.RIGHT_DRIVE_DEVICE_ID,      MOTOR_MODES.K_PERCENT_VBUS)
collectorDepthMotor  = Motor("CollectorDepthMotor",  CONSTANTS.COLLECTOR_DEPTH_DEVICE_ID,  MOTOR_MODES.K_PERCENT_VBUS)
collectorScoopsMotor = Motor("CollectorScoopsMotor", CONSTANTS.COLLECTOR_SCOOPS_DEVICE_ID, MOTOR_MODES.K_PERCENT_VBUS)
winchMotor           = Motor("WinchMotor",           CONSTANTS.WINCH_DEVICE_ID,            MOTOR_MODES.K_PERCENT_VBUS)

# initialize motor handler and add motors
motorHandler.addMotor(leftDriveMotor)
motorHandler.addMotor(rightDriveMotor)
motorHandler.addMotor(collectorDepthMotor)
motorHandler.addMotor(collectorScoopsMotor)
motorHandler.addMotor(winchMotor)

# initialize sensors
leftDriveCurrentSense = Sensor("LeftDriveCurrentSense")
rightDriveCurrentSense = Sensor("RightDriveCurrentSense")
collectorDepthCurrentSense = Sensor("CollectorDepthCurrentSense")
collectorScoopsCurrentSense = Sensor("CollectorScoopsCurrentSense")
winchMotorCurrentSense = Sensor("WinchMotorCurrentSense")

scoopReedSwitch = Sensor("ScoopReedSwitch")
bucketMaterialDepthSense = Sensor("BucketMaterialDepthSense")

# initialize sensor handler and add sensors
sensorHandler.addSensor(leftDriveCurrentSense)
sensorHandler.addSensor(rightDriveCurrentSense)
sensorHandler.addSensor(collectorDepthCurrentSense)
sensorHandler.addSensor(collectorScoopsCurrentSense)
sensorHandler.addSensor(winchMotorCurrentSense)
sensorHandler.addSensor(scoopReedSwitch)
sensorHandler.addSensor(bucketMaterialDepthSense)

# initialize robotState
robotState = RobotState()

# initialize joystick, if using joystick
if CONSTANTS.USING_JOYSTICK:
	pygame.init()
	pygame.joystick.init()
	joystick1 = pygame.joystick.Joystick(0)
	joystick1.init()
	jReader = JoystickReader(joystick1)
	
if CONSTANTS.USING_MOTOR_BOARD:
	motorCommThread = Thread(target=motorCommunicationThread)
	motorCommThread.start()

if CONSTANTS.USING_SENSOR_BOARD:
	sensorCommThread = Thread(target=sensorCommunicationThread)
	sensorCommThread.start()

# final line before entering main loop
robotEnabled = True
time.sleep(0.5)

while robotEnabled:

	loopStartTime = time.time()
	print strftime("%H:%M:%S.", gmtime()) + str(int((time.time()*1000) % 1000)) + ": ",

	currentState = robotState.getState()
	lastState = robotState.getLastState()

	'''
	# +----------------------------------------------+
	# |              Current State Logic             |
	# +----------------------------------------------+
	# State machine handles the robot's current states
	
	if(currentState == "OFF"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	elif(currentState == "ROTATE_TO_MARKER"):
		pass
		#rotate motors according to camera

	elif(currentState == "DRIVE_TO_DIG_AREA"):
		leftDriveMotor.setSpeed(CONSTANTS.DRIVE_SPEED)
		rightDriveMotor.setSpeed(-CONSTANTS.DRIVE_SPEED)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	elif(currentState == "STOP_AT_DIG_AREA"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	elif(currentState == "RUN_SCOOPS"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(CONSTANTS.SCOOP_SPEED)
		collectorDepthMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	elif(currentState == "INCREMENT_DEPTH"):
		collectorDepthMotor.setSpeed(CONSTANTS.DEPTH_SPEED)

	elif(currentState == "DECREMENT_DEPTH"):
		collectorDepthMotor.setSpeed(-CONSTANTS.DEPTH_SPEED)

	elif(currentState == "STOP_SCOOPS"):
		collectorScoopsMotor.setSpeed(0)

	elif(currentState == "DRIVE_TO_COLLECTION_BIN"):
		leftDriveMotor.setSpeed(-CONSTANTS.DRIVE_SPEED)
		rightDriveMotor.setSpeed(CONSTANTS.DRIVE_SPEED)

	elif(currentState == "STOP_AT_COLLECTION_BIN"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)

	elif(currentState == "RAISE_BUCKET"):
		winchMotor.setSpeed(CONSTANTS.WINCH_SPEED)

	elif(currentState == "LOWER_BUCKET"):
		winchMotor.setSpeed(-CONSTANTS.WINCH_SPEED)

	elif(currentState == "TELEOP_CONTROL"):
		#do teleop
		pass

	else: # error state, set errything to off
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	# +----------------------------------------------+
	# |               Next State Logic               |
	# +----------------------------------------------+
	# Conditionals to determine the next state
	if(currentState == "OFF"):
		
		# if last state was 'None', robot is just starting
		if(lastState == None):
			robotState.setState("ROTATE_TO_MARKER");

	elif(currentState == "ROTATE_TO_MARKER"):
		pass
		# if marker is found, rotate towards dig area

	'''
	
	leftDriveMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	rightDriveMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	collectorDepthMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	collectorScoopsMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	winchMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	
	if CONSTANTS.USING_JOYSTICK:
		pygame.event.get()
		jReader.updateValues()
		leftDriveMotor.setSpeed(-jReader.axis_y1)
		rightDriveMotor.setSpeed(jReader.axis_y2)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)
	
	else:
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)
		
	print leftDriveMotor.current_val
	# +----------------------------------------------+
	# |          Communication & Updates             |
	# +----------------------------------------------+
	# Update the motor values locally, then send new values over
	# serial --- handled via threading



	#if(not outboundMessageQueue.isEmpty()):
	#	outboundMessageQueue.makeEmpty()
	#outboundMessageQueue.add("Here is a response")
	


	#sleep to maintain a more constant thread time (specified in Constants.py)
	loopEndTime = time.time()
	loopExecutionTime = loopEndTime - loopStartTime
	sleepTime = CONSTANTS.LOOP_DELAY_TIME - loopExecutionTime
	if(sleepTime > 0):
		time.sleep(sleepTime)
		
	print ""

