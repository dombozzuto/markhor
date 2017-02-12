class Sensor:

	def __init__(self, name):
		self.sensorName = name
		self.value = 0

	def getValue(self):
		return self.value

	def getSensorName(self):
		return self.sensorName

	def updateValue(self, newValue):
		self.value = newValue
		print "Value of sensor <" + self.sensorName + "> was updated to " + str(self.value)

