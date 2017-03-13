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

	#networkHandler = NetworkHandler(inboundMessageQueue, outboundMessageQueue)
	#server = SocketServer.TCPServer((CONSTANTS.HOST, CONSTANTS.PORT), networkHandler)
	#serverThread = Thread(target=runServer, args=(server,))
	#serverThread.start()




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
while robotEnabled:

	loopStartTime = time.time()
	#print strftime("%H:%M:%S.", gmtime()) + str(int((time.time()*1000) % 1000)) + ": ",

	currentState = robotState.getState()
	lastState = robotState.getLastState()

	
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
			
			robotState.setState(currentMessage.type)
			
			if(currentMessage.type == "MSG_STOP"):
				LOGGER.Debug("Received a MSG_STOP")
				
			
			elif(currentMessage.type == "MSG_DRIVE_TIME"):
				LOGGER.Debug("Received a MSG_DRIVE_TIME")
			
			elif(currentMessage.type == "MSG_DRIVE_DISTANCE"):
				LOGGER.Debug("Received a MSG_DRIVE_DISTANCE")
			
			else:
				LOGGER.Low("Received an invalid message.")
				
	
	
	leftDriveMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	rightDriveMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	collectorDepthMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	collectorScoopsMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	winchMotor.setMode(MOTOR_MODES.K_PERCENT_VBUS)
	
	if CONSTANTS.USING_JOYSTICK:
		pygame.event.get()
		jReader.updateValues()
		leftDriveMotor.setSpeed(jReader.axis_y1)
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
		
	# +----------------------------------------------+
	# |                Communication                 |
	# +----------------------------------------------+

	if CONSTANTS.USING_NETWORK_COMM:
		networkClient.send("Hello World")
		#BEEPCODES.heartbeat()


	


	#sleep to maintain a more constant thread time (specified in Constants.py)
	loopEndTime = time.time()
	loopExecutionTime = loopEndTime - loopStartTime
	sleepTime = CONSTANTS.LOOP_DELAY_TIME - loopExecutionTime
	if(sleepTime > 0):
		time.sleep(sleepTime)

