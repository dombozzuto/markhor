import time
import SocketServer
import threading
import pygame
from threading import Thread

import Constants as CONSTANTS
from Constants import LOGGER
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
from NetworkClient import NetworkClient
from NetworkMessage import NetworkMessage
import BeepCodes as BEEPCODES

from time import gmtime, strftime
#from main import inboundMessageQueue

LOGGER.Low("Beginning Program Execution")

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
		
def ceaseAllMotorFunctions():
	leftDriveMotor.setSpeed(0)
	rightDriveMotor.setSpeed(0)
	collectorDepthMotor.setSpeed(0)
	collectorScoopsMotor.setSpeed(0)
	winchMotor.setSpeed(0)

#initialize handlers
LOGGER.Debug("Initializing handlers...")
motorHandler = MotorHandler()
sensorHandler = SensorHandler()

if CONSTANTS.USING_MOTOR_BOARD:
	LOGGER.Debug("Initializing motor serial handler...")
	motorSerialHandler = SerialHandler(CONSTANTS.MOTOR_BOARD_PORT)
	motorSerialHandler.initSerial()
	
if CONSTANTS.USING_SENSOR_BOARD:
	LOGGER.Debug("Initializing sensor serial handler...")
	sensorSerialHandler = SerialHandler(CONSTANTS.SENSOR_BOARD_PORT)
	sensorSerialHandler.initSerial()

#initialize network comms & server thread
if CONSTANTS.USING_NETWORK_COMM:
	networkClient = NetworkClient(CONSTANTS.CONTROL_STATION_IP, CONSTANTS.CONTROL_STATION_PORT)
	inboundMessageQueue = MessageQueue()
	networkClient.setInboundMessageQueue(inboundMessageQueue)
	outboundMessageQueue = MessageQueue()
	lastReceivedMessageNumber = -1
	currentReceivedMessageNumber = -1
	stateStartTime = -1

	#networkHandler = NetworkHandler(inboundMessageQueue, outboundMessageQueue)
	#server = SocketServer.TCPServer((CONSTANTS.HOST, CONSTANTS.PORT), networkHandler)
	#serverThread = Thread(target=runServer, args=(server,))
	#serverThread.start()


# setup some variables that will be used with each iteration of the loop
currentMessage = NetworkMessage("")

# initialize motors
LOGGER.Debug("Initializing motor objects...")
leftDriveMotor       = Motor("LeftDriveMotor",       CONSTANTS.LEFT_DRIVE_DEVICE_ID,       MOTOR_MODES.K_PERCENT_VBUS)
rightDriveMotor      = Motor("RightDriveMotor",      CONSTANTS.RIGHT_DRIVE_DEVICE_ID,      MOTOR_MODES.K_PERCENT_VBUS)
collectorDepthMotor  = Motor("CollectorDepthMotor",  CONSTANTS.COLLECTOR_DEPTH_DEVICE_ID,  MOTOR_MODES.K_PERCENT_VBUS)
collectorScoopsMotor = Motor("CollectorScoopsMotor", CONSTANTS.COLLECTOR_SCOOPS_DEVICE_ID, MOTOR_MODES.K_PERCENT_VBUS)
winchMotor           = Motor("WinchMotor",           CONSTANTS.WINCH_DEVICE_ID,            MOTOR_MODES.K_PERCENT_VBUS)

# initialize motor handler and add motors
LOGGER.Debug("Linking motors to motor handler...")
motorHandler.addMotor(leftDriveMotor)
motorHandler.addMotor(rightDriveMotor)
motorHandler.addMotor(collectorDepthMotor)
motorHandler.addMotor(collectorScoopsMotor)
motorHandler.addMotor(winchMotor)

# initialize sensors
LOGGER.Debug("Initializing sensor objects...")
leftDriveCurrentSense = Sensor("LeftDriveCurrentSense")
rightDriveCurrentSense = Sensor("RightDriveCurrentSense")
collectorDepthCurrentSense = Sensor("CollectorDepthCurrentSense")
collectorScoopsCurrentSense = Sensor("CollectorScoopsCurrentSense")
winchMotorCurrentSense = Sensor("WinchMotorCurrentSense")
scoopReedSwitch = Sensor("ScoopReedSwitch")
bucketMaterialDepthSense = Sensor("BucketMaterialDepthSense")

# initialize sensor handler and add sensors
LOGGER.Debug("Linking sensor objects to sensor handler...")
sensorHandler.addSensor(leftDriveCurrentSense)
sensorHandler.addSensor(rightDriveCurrentSense)
sensorHandler.addSensor(collectorDepthCurrentSense)
sensorHandler.addSensor(collectorScoopsCurrentSense)
sensorHandler.addSensor(winchMotorCurrentSense)
sensorHandler.addSensor(scoopReedSwitch)
sensorHandler.addSensor(bucketMaterialDepthSense)

# initialize robotState
LOGGER.Debug("Initializing robot state...")
robotState = RobotState()

# initialize joystick, if using joystick
if CONSTANTS.USING_JOYSTICK:
	LOGGER.Debug("Initializing joystick...")
	pygame.init()
	pygame.joystick.init()
	joystick1 = pygame.joystick.Joystick(0)
	joystick1.init()
	jReader = JoystickReader(joystick1)
	
if CONSTANTS.USING_MOTOR_BOARD:
	LOGGER.Debug("Initializing motor board thread...")
	motorCommThread = Thread(target=motorCommunicationThread)
	motorCommThread.daemon = True
	motorCommThread.start()

if CONSTANTS.USING_SENSOR_BOARD:
	LOGGER.Debug("Initializing sensor board thread...")
	sensorCommThread = Thread(target=sensorCommunicationThread)
	sensorCommThread.daemon = True
	sensorCommThread.start()

# final line before entering main loop
robotEnabled = True
time.sleep(0.5)
BEEPCODES.happy1()
LOGGER.Debug("Initialization complete, entering main loop...")

test_speed_val = -1.0
while robotEnabled:

	loopStartTime = time.time()
	#print strftime("%H:%M:%S.", gmtime()) + str(int((time.time()*1000) % 1000)) + ": ",

	currentState = robotState.getState()
	lastState = robotState.getLastState()

	# +----------------------------------------------+
	# |                Communication                 |
	# +----------------------------------------------+

	if CONSTANTS.USING_NETWORK_COMM:
		connected = False
		while(not connected):
			try:
				if(outboundMessageQueue.isEmpty()):
					networkClient.send("Hello World\n")
				else:
					networkClient.send(outboundMessageQueue.getNext())
				connected = True
			except:
				LOGGER.Critical("Could not connect to network, attempting to reconnect...")
				ceaseAllMotorFunctions()
		#BEEPCODES.heartbeat()

	
	# +----------------------------------------------+
	# |              Current State Logic             |
	# +----------------------------------------------+
	# State machine handles the robot's current states
	if CONSTANTS.USING_NETWORK_COMM:
		
		if(not inboundMessageQueue.isEmpty()):
			currentMessage = inboundMessageQueue.getNext()
			lastReceivedMessageNumber = currentReceivedMessageNumber
			currentReceivedMessageNumber = currentMessage.messageNumber
			
		#new message has arrived, process
		if(lastReceivedMessageNumber != currentReceivedMessageNumber):
			
			stateStartTime = time.time()
			robotState.setState(currentMessage.type)
			print currentMessage.type
			
			if(currentMessage.type == "MSG_STOP"):
				LOGGER.Debug("Received a MSG_STOP")
				
			elif(currentMessage.type == "MSG_DRIVE_TIME"):
				LOGGER.Debug("Received a MSG_DRIVE_TIME")
				
			elif(currentMessage.type == "MSG_SCOOP_TIME"):
				LOGGER.Debug("Received a MSG_SCOOP_TIME")
				
			elif(currentMessage.type == "MSG_DEPTH_TIME"):
				LOGGER.Debug("Received a MSG_DEPTH_TIME")
				
			elif(currentMessage.type == "MSG_BUCKET_TIME"):
				LOGGER.Debug("Received a MSG_BUCKET_TIME")
			
			elif(currentMessage.type == "MSG_DRIVE_DISTANCE"):
				LOGGER.Debug("Received a MSG_DRIVE_DISTANCE")
				leftDriveMotor.setMode(MOTOR_MODES.K_SPEED)
				rightDriveMotor.setMode(MOTOR_MODES.K_SPEED)
				startingDistance = 0 #TODO get distance from encoders
				
			elif(currentMessage.type == "MSG_MOTOR_VALUES"):
				LOGGER.Debug("Received a MSG_MOTOR_VALUES")
				print "MADE IT 1"
			else:
				LOGGER.Moderate("Received an invalid message.")
				
		#
		# MSG_STOP:
		# Stop all motors immediately
		#
		if(currentMessage.type == "MSG_STOP"):
			ceaseAllMotorFunctions()
			outboundMessageQueue.add("Finished\n")
		
		#
		# MSG_DRIVE_TIME:
		# Drive forward/backward with both motors at the same value
		# Data 0: The time in seconds the robot should drive
		# Data 1: The power/speed to drive at
		#
		elif(currentMessage.type == "MSG_DRIVE_TIME"):
			currentMessage.printMessage()
			if(time.time() < stateStartTime + currentMessage.messageData[0]):
				driveSpeed = currentMessage.messageData[1]
				leftDriveMotor.setSpeed(driveSpeed)
				rightDriveMotor.setSpeed(-driveSpeed)
			else:
				ceaseAllMotorFunctions()
				outboundMessageQueue.add("Finished\n")
		#
		# MSG_SCOOP_TIME:
		# Drive the scoops for a set time at a specified speed
		# Data 0: The time in seconds the scoop motor should run
		# Data 1: The power/speed to run the motor at
		#		
		elif(currentMessage.type == "MSG_SCOOP_TIME"):
			currentMessage.printMessage()
			if(time.time() < stateStartTime + currentMessage.messageData[0]):
				scoopSpeed = currentMessage.messageData[1]
				collectorScoopsMotor.setSpeed(scoopSpeed)
			else:
				ceaseAllMotorFunctions()
				outboundMessageQueue.add("Finished\n")
		#
		# MSG_DEPTH_TIME:
		# Drive the depth motor for a set time at a specified power/speed
		# Data 0: The time in seconds the depth motor should run
		# Data 1: The power/speed to run the motor at
		#			
		elif(currentMessage.type == "MSG_DEPTH_TIME"):
			currentMessage.printMessage()
			if(time.time() < stateStartTime + currentMessage.messageData[0]):
				depthSpeed = currentMessage.messageData[1]
				collectorDepthMotor.setSpeed(depthSpeed)
			else:
				ceaseAllMotorFunctions()
				outboundMessageQueue.add("Finished\n")
		#
		# MSG_BUCKET_TIME:
		# Drive the bucket for a set time at a specified speed
		# Data 0: The time in seconds the bucket motor should run
		# Data 1: The power/speed to run the motor at
		#			
		elif(currentMessage.type == "MSG_BUCKET_TIME"):
			currentMessage.printMessage()
			if(time.time() < stateStartTime + currentMessage.messageData[0]):
				bucketSpeed = currentMessage.messageData[1]
				winchMotor.setSpeed(bucketSpeed)
			else:
				ceaseAllMotorFunctions()
				outboundMessageQueue.add("Finished\n")
		
				
		elif(currentMessage.type == "MSG_DRIVE_DISTANCE"):
			if(leftDriveMotor.getDistance() > startingDistance + currentMessage.messageData[0]):
				driveSpeed = currentMessage.messageData[1]
				leftDriveMotor.setSpeed(driveSpeed)
				rightDriveMotor.setSpeed(-driveSpeed)	
			else:
				ceaseAllMotorFunctions()
				outboundMessageQueue.add("Finished\n")
			
		elif(currentMessage.type == "MSG_MOTOR_VALUES"):
			leftDriveMotor.setSpeed(currentMessage.messageData[0])
			rightDriveMotor.setSpeed(currentMessage.messageData[1])
			collectorScoopsMotor.setSpeed(currentMessage.messageData[2])
			collectorDepthMotor.setSpeed(currentMessage.messageData[3])
			winchMotor.setSpeed(currentMessage.messageData[4])
	#will be removed
	leftDriveMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	rightDriveMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	collectorDepthMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	collectorScoopsMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	winchMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	
	if CONSTANTS.USING_JOYSTICK:
		#pygame.event.get()
		#jReader.updateValues()
		#leftDriveMotor.setSpeed(jReader.axis_y1)
		#rightDriveMotor.setSpeed(jReader.axis_y2)
		leftDriveMotor.setSpeed(1.0)
		rightDriveMotor.setSpeed(-1.0)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)
	
#	else:
#		if(test_speed_val > 1.0):
#			test_speed_val = 0
#		else:
#			test_speed_val += 0.001
#		test_speed_val += 0.001
		#leftDriveMotor.setSpeed(0)
		#rightDriveMotor.setSpeed(0)
		#collectorDepthMotor.setSpeed(0)
		#collectorScoopsMotor.setSpeed(0)
		#winchMotor.setSpeed(0)
		
	#sleep to maintain a more constant thread time (specified in Constants.py)
	loopEndTime = time.time()
	loopExecutionTime = loopEndTime - loopStartTime
	sleepTime = CONSTANTS.LOOP_DELAY_TIME - loopExecutionTime
	if(sleepTime > 0):
		time.sleep(sleepTime)



