import re
import Constants as CONSTANTS
from Constants import LOGGER
import MotorModes as MOTOR_MODES
import RobotPose as rpos
import Motor

class AutonomousDrive:
	''' Manages performing the calculations to find the directions to goal position 
	'''
	def __init__(self):
		self.currentPose = rpos.RobotPose();
		self.previousPose = rpos.RobotPose();
		self.targetPose = rpos.RobotPose();

	# gets the target angle relative to world
	def calculateAngle(target_pose):
		pass;

	# returns distance to goal
	def calculateDistToGo(target_pose):
		pass;

	# returns the target angle and distance to go til goal is met
	def calculateStep(target_pose):
		t_q = calculateAngle(target_pose);
		t_d = calculateDistToGo(target_pose);
		pass;

def main():
	ad = AutonomousDrive();
	print ad.currentPose.x;

if __name__ == '__main__':
	main();