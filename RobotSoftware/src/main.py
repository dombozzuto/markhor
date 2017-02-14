import Constants as CONSTANTS
import MotorModes as MOTOR_MODES

from Motor import Motor
from MotorHandler import MotorHandler
from Sensor import Sensor
from SensorHandler import SensorHandler
from RobotState import RobotState
from SerialHandler import SerialHandler

import time
from time import gmtime, strftime

# initialization:
# CAN Bus Device IDs


#initialize handlers
motorHandler = MotorHandler()
sensorHandler = SensorHandler()

#motorSerialHandler = SerialHandler('COM4')
sensorSerialHandler = SerialHandler('COM3')

sensorSerialHandler.initSerial()

# initialize motors
leftDriveMotor       = Motor("LeftDriveMotor",       CONSTANTS.LEFT_DRIVE_DEVICE_ID,       MOTOR_MODES.SPEED)
rightDriveMotor      = Motor("RightDriveMotor",      CONSTANTS.RIGHT_DRIVE_DEVICE_ID,      MOTOR_MODES.SPEED)
collectorDepthMotor  = Motor("CollectorDepthMotor",  CONSTANTS.COLLECTOR_DEPTH_DEVICE_ID,  MOTOR_MODES.SPEED)
collectorScoopsMotor = Motor("CollectorScoopsMotor", CONSTANTS.COLLECTOR_SCOOPS_DEVICE_ID, MOTOR_MODES.SPEED)
winchMotor           = Motor("WinchMotor",           CONSTANTS.WINCH_DEVICE_ID,            MOTOR_MODES.SPEED)

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

# final line before entering main loop
robotEnabled = True
time.sleep(0.5)

while robotEnabled:

	loopStartTime = time.time()
	print strftime("%H:%M:%S.", gmtime()) + str(int((time.time()*1000) % 1000))

	currentState = robotState.getState()
	lastState = robotState.getLastState()

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


	# +----------------------------------------------+
	# |          Communication & Updates             |
	# +----------------------------------------------+
	# Update the motor values locally, then send new values over
	# serial
	#inboundMotorMessage = motorSerialHandler.getMessage()
	#motorHandler.updateMotors(inboundMotorMessage)
	#outboundMotorMessage = motorHandler.getMotorStateMessage()
	#motorSerialHandler.sendMessage(outboundMotorMessage)

	# Update the sensor values locally
	inboundSensorMessage = sensorSerialHandler.getMessage()
	sensorHandler.updateSensors(inboundSensorMessage)



	#sleep to maintain a more constant thread time (specified in Constants.py)
	loopEndTime = time.time()
	loopExecutionTime = loopEndTime - loopStartTime
	sleepTime = CONSTANTS.LOOP_DELAY_TIME - loopExecutionTime
	if(sleepTime > 0):
		time.sleep(sleepTime)

