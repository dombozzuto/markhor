class RobotState:

	self.currentState = None
	self.lastState = None

	def __init__(self):
		self.currentState = "OFF"
		self.lastState = None

	def getState(self):
		return self.currentState()

	def getLastState(self):
		return self.lastState()

	def setState(self, state):
		self.lastState = self.currentState
		self.currentState = state

