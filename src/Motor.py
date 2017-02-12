from CanTalonSRX import *
import can

class Motor:

	def __init__(self, devID, canBus):
		self.deviceID = devID
		self.bus = canBus
		self.speed = 0
		self.direction = 0
		self.talon = CanTalonSRX(self.deviceID)
		self.talon.set_mode(Mode.DutyCycle)

	def update(self):

		if not self.talon.txQueue.empty():
			msg = talon.txQueue.get_nowait()
			msg.timestamp = time.time()
			self.bus.send(msg)

		recv = bus.recv(0.0)
		if recv != None:
			motor.talon.update(recv)

	#set the speed of the motor from -1.0 to 1.0
	def setSpeed(self, speed):
		self.speed = speed
		self.talon.set_throttle(self.speed)

	