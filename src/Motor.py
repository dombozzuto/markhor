class Motor:

	def __init__(self, devID, mode):
		self.deviceID = devID
		self.setpoint_val = 0
		self.actual_val = 0
		self.mode = mode
		self.forward_limit = False
		self.reverse_limit = False

	'''
	Takes a string representing containing motor information
	If the device ID of this motor matches the string, update the values
	accordingly.  If it does not match, ignore the message. Similarly, if
	the message is invald, ignore it
	'''
	def update(self, update_info):
		# remove the < and >
		message = message[1:-1]

		# split the message meaningful parts
		message_parts = message.split(":")

		if(len(message_parts) < 2):
			print "ERROR: Message has too few components and is probably malformed. Device ID: " + str(self.deviceID)
			return None


		# be ready to throw an error
		try:
			#try to read all the values before assigning anything
			msg_deviceID = int(message_parts[0])
			msg_feedback_val = int(message_parts[1])
			msg_forward_limit = bool(int(message_parts[2]))
			msg_reverse_limit = bool(int(message_parts[3]))

			if(msg_deviceID == self.deviceID):
				self.forward_limit = msg_forward_limit
				self.reverse_limit = msg_reverse_limit
				self.actual_val = msg_feedback_val

		except:
			print "ERROR: Unable to parse one or more of the message components. Device ID: " + str(self.deviceID)

	#set the speed of the motor from -1.0 to 1.0
	def setSpeed(self, speed):
		self.setpoint_val = speed

	def formMessage(self):
		return "<" + str(deviceID) + ":" + str(mode) + ":" + str(setpoint) + ">"


	