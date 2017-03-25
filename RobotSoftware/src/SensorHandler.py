class SensorHandler:

	def __init__(self):
		self.sensors = []

	def addSensor(self, sensor):
		self.sensors.append(sensor)

	def updateSensors(self, update_msg):
		for sensor in self.sensors:
			sensor.update(update_msg)

	def printSensorValues(self):
		print self.getSensorValues()
	
	def getSensorValues(self):
		sensorMsg = ""
		for sensor in self.sensors:
			sensorMsg += str(sensor.getValue()) + '|';
		return sensorMsg

	def getSensorDataMessage(self):
		msg = ""
		for sensor in self.sensors:
			msg += sensor.getDataMessage()
		return msg



