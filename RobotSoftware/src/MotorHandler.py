import time

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
	
	def getNetworkMotorData(self):
		msg_setpoints = "<"
		msg_actuals = "<"
		msg_currents = "<"
		msg_modes = "<"
		for i in range(len(self.motors)):
			msg_setpoints += str(self.motors[i].setpoint_val)
			msg_actuals += str(self.motors[i].actual_val)
			msg_currents += str(self.motors[i].current_val)
			msg_modes += str(self.motors[i].mode)
			
			if(i != (len(self.motors) - 1 )):
				msg_setpoints += ","
				msg_actuals += ","
				msg_currents += ","
				msg_modes += ","
				
		msg_setpoints += ">"
		msg_actuals += ">"
		msg_currents += ">"
		msg_modes += ">"
		
		return msg_setpoints + "," + msg_actuals + "," + msg_currents + "," + msg_modes + ","
			
			
