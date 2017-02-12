from Motor import Motor
from MotorHandler import MotorHandler
from Sensor import Sensor
from SensorHandler import SensorHandler

# initialization:
# CAN Bus Device IDs
leftDriveDeviceID = 0
rightDriveDeviceID = 1
collectorDepthDeviceID = 2
collectorScoopsDeviceID = 3
winchDeviceID = 4

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