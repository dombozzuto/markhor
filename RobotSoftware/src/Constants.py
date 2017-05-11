import Logger

SENSOR_BOARD_PORT = "/dev/ttyACM0"
MOTOR_BOARD_PORT = "/dev/ttyUSB0"
CONTROL_STATION_IP = "192.168.0.100"
CONTROL_STATION_PORT = 11000
CAMERA_PORT1 = 11001

USING_MOTOR_BOARD = True
USING_SENSOR_BOARD = True
USING_NETWORK_COMM = True
USING_JOYSTICK = False

MAX_SPEED = 1.0
MIN_SPEED = -1.0

DRIVE_SPEED = 0.75
SCOOP_SPEED = 0.75
DEPTH_SPEED = 0.05
WINCH_SPEED = 1.00

LEFT_DRIVE_DEVICE_ID = 1
RIGHT_DRIVE_DEVICE_ID = 2
COLLECTOR_DEPTH_DEVICE_ID = 4
COLLECTOR_SCOOPS_DEVICE_ID = 3
WINCH_DEVICE_ID = 5

LOOP_DELAY_TIME = 0.050

HOST = "localhost"
PORT = 9999

ON_LINUX = True

LOG_CRITICAL = 1
LOG_SEVERE = 2
LOG_MODERATE = 3
LOG_LOW = 4
LOG_DEBUG = 5

LOGGER = Logger.Logger(LOG_LOW)