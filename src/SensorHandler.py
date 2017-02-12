import serial
import io
import re
import time
import logging

class SensorHandler:

	def __init__(self, port):
		self.ser = serial.Serial()
		self.sensors = []
		self.ser.baudrate = 9600
		self.ser.port = port
		self.initSerial()


	def initSerial(self):
		print "Attempting to open serial port: " + str(self.ser.port)
		for i in range(3):
			try:
				self.ser.open()
				print "SUCCESS: Serial port opened on port: " + str(self.ser.port)
				return;
			except:
				print "FAILED: Open serial on port: " + str(self.ser.port)
				print "Retry in 5 seconds"
				time.sleep(5)

		print "CRITICAL FAILURE: Unable to open serial on port: " + str(self.ser.port)

	def addSensor(self, sensor):
		self.sensors.append(sensor)

	def read(self):
		if(self.ser.is_open):
			line = self.ser.readline()
			self.parseAndUpdate(line)

	def parseAndUpdate(self, line):

		# split the string into tokens, the remove '<>\n'
		# TODO: Rewrite properly with regex
		tokens = line.split('>')
		new_tokens = []
		for token in tokens:
			new_token1 = token.replace('<', '')
			new_token2 = new_token1.replace('>', '')
			new_token3 = new_token2.replace('\n', '')
			if(len(new_token3) > 0):
				new_tokens.append(new_token2)
		tokens = new_tokens

		sensors_and_values = []

		# split the messages to [[sensorName],[value]]
		for token in tokens:
			sub_tokens = token.split(':')
			sensors_and_values.append(sub_tokens)

		# match sensorName with existing sensors and update sensor object values
		for s in range(len(sensors_and_values)):
			for sensor in self.sensors:
				if(sensor.getSensorName() == sensors_and_values[s][0]):
					sensor.updateValue(int(sensors_and_values[s][1]))

		




