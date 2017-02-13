import Constants as CONSTANTS

from Motor import Motor
from MotorHandler import MotorHandler
from Sensor import Sensor
from SensorHandler import SensorHandler
from RobotState import RobotState

# initialization:
# CAN Bus Device IDs
leftDriveDeviceID = 1
rightDriveDeviceID = 2
collectorDepthDeviceID = 3
collectorScoopsDeviceID = 4
winchDeviceID = 5

#initialize handlers
motorHandler = MotorHandler()
sensorHandler = SensorHandler('COM3')

# initalize motors
leftDriveMotor = Motor(leftDriveDeviceID)
rightDriveMotor = Motor(rightDriveDeviceID)
collectorDepthMotor = Motor(collectorDepthDeviceID)
collectorScoopsMotor = Motor(collectorScoopsDeviceID)
winchMotor = Motor(winchDeviceID)

# initialize motor handler and add motors
motorHandler.addMotor(leftDriveMotor, motorHandler.getBus())
motorHandler.addMotor(rightDriveMotor, motorHandler.getBus())
motorHandler.addMotor(collectorDepthMotor, motorHandler.getBus())
motorHandler.addMotor(collectorScoopsMotor, motorHandler.getBus())
motorHandler.addMotor(winchMotor, motorHandler.getBus())

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
RobotState robotState = RobotState()



# final line before entering main loop
robotEnabled = True

while robotEnabled:

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

	else if(currentState == "ROTATE_TO_MARKER"):
		#rotate motors according to camera

	else if(currentState == "DRIVE_TO_DIG_AREA"):
		leftDriveMotor.setSpeed(CONSTANTS.DRIVE_SPEED)
		rightDriveMotor.setSpeed(-CONSTANTS.DRIVE_SPEED)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	else if(currentState == "STOP_AT_DIG_AREA"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorDepthMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	else if(currentState == "RUN_SCOOPS"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)
		collectorScoopsMotor.setSpeed(CONSTANTS.SCOOP_SPEED)
		collectorDepthMotor.setSpeed(0)
		winchMotor.setSpeed(0)

	else if(currentState == "INCREMENT_DEPTH"):
		collectorDepthMotor.setSpeed(CONSTANTS.DEPTH_SPEED)

	else if(currentState == "DECREMENT_DEPTH"):
		collectorDepthMotor.setSpeed(-CONSTANTS.DEPTH_SPEED)

	else if(currentState == "STOP_SCOOPS"):
		collectorScoopsMotor.setSpeed(0)

	else if(currentState == "DRIVE_TO_COLLECTION_BIN"):
		leftDriveMotor.setSpeed(-CONSTANTS.DRIVE_SPEED)
		rightDriveMotor.setSpeed(CONSTANTS.DRIVE_SPEED)

	else if(currentState == "STOP_AT_COLLECTION_BIN"):
		leftDriveMotor.setSpeed(0)
		rightDriveMotor.setSpeed(0)

	else if(currentState == "RAISE_BUCKET"):
		winchMotor.setSpeed(CONSTANTS.WINCH_SPEED)

	else if(currentState == "LOWER_BUCKET"):
		winchMotor.setSpeed(-CONSTANTS.WINCH_SPEED)

	else if(currentState == "TELEOP_CONTROL"):
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

	else if(currentState == "ROTATE_TO_MARKER"):

		# if marker is found, rotate towards dig area
