import serial
import io
import re
import time
import logging
import sys

class SensorHandler:

	def __init__(self):
		self.sensors = []


	def addSensor(self, sensor):
		self.sensors.append(sensor)

	def updateSensors(self, update_msg):
		for sensor in self.sensors:
			sensor.update(update_msg)

	




