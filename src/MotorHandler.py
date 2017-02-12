import time
import can

class MotorHandler:

	def __init__(self):
		self.bus = can.interface.Bus()
		self.motors = []

	def getBus(self):
		return self.bus

	def addMotor(self, motor):
		self.motors.append(motor)

	def updateMotors(self):
		for motor in self.motors:
			motor.update()

	def run(self):
		self.updateMotors()
