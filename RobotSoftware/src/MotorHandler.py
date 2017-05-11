import time
from Constants import LOGGER

class MotorHandler:

	def __init__(self):
		self.motors = []

	def addMotor(self, motor):
		self.motors.append(motor)

	def updateMotors(self, update_msg):
		for motor in self.motors:
			motor.update(update_msg)

	def getMotorStateMessage(self):
		msg = ""
		for motor in self.motors:
			msg += motor.getStateMessage()
		msg += "\n\r"
		return msg

	def getMotorByteMessage(self):
		msg_bytes = b''
		start_bytes  = b'\xDE\xAD'
		end_bytes = b'\xBE\xEF'
		msg_bytes = b''.join([msg_bytes, start_bytes])
		for motor in self.motors:
			msg_bytes = b''.join([msg_bytes, motor.getByteMessage()])
		msg_bytes = b''.join([msg_bytes, end_bytes])
		return msg_bytes
	
	def getMotorNetworkMessage(self):
		msg = ""
		for motor in self.motors:
			msg += motor.getNetworkMessage()
		return msg