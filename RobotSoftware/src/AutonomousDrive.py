import re
import Constants as CONSTANTS
from Constants import LOGGER
import MotorModes as MOTOR_MODES
import RobotPose as rp
import Motor
import math
import numpy as np
from numpy import linalg as LA

class AutonomousDrive:
	''' Manages performing the calculations to find the directions to goal position 
	'''
	def __init__(self, target_pose = rp.RobotPose(CONSTANTS.TF_TARGET_ORIENTATION, 
		CONSTANTS.TF_TARGET_POSITION)):
		self.currentPose = rp.RobotPose();
		self.previousPose = rp.RobotPose();
		self.targetPose = target_pose;

	#getter for current pose
	def getCurrentPose(self):
		return self.currentPose;

	#setter for current pose
	def setCurrentPose(self, newCurrentPose):
		self.currentPose = newCurrentPose;

	#getter for current pose
	def getPreviousPose(self):
		return self.previousPose;

	#setter for current pose
	def setPreviousPose(self, newPreviousPose):
		self.previousPose = newPreviousPose;

	#getter for current pose
	def getTargetPose(self):
		return self.targetPose;

	#setter for current pose
	def setTargetPose(self, newTargetPose):
		self.targetPose = newTargetPose;

	# calculates the tf from world to robot
	# tf_world_cam is the transform from cam relative to world
	# panTheta is the orientation of camera to the robot, radians
	def calculateTfWorldToRobot(self, tf_world_cam, panTheta):
		camEulerAngles = [0, panTheta, 0]; # [x, y, z] axis rotation
		R_cam_robot = rp.eulerAnglesToRotationMatrix(camEulerAngles);
		tf_cam_robot = rp.constructTfMat(R_cam_robot, CONSTANTS.TF_CAM_ROBOT_POSITION); 
		tf_world_robot = np.dot(tf_world_cam, tf_cam_robot);
		return tf_world_robot;

	# returns distance to goal
	def calculateDistToGo(self, tf_world_cam, panTheta):
		tf_world_robot = self.calculateTfWorldToRobot(tf_world_cam, panTheta)
		v_world_robot = tf_world_robot[np.ix_([0, 1, 2],[3])];
		v_world_target = CONSTANTS.TF_TARGET_POSITION;
		# gets vector from robot to target
		v_robot_target = np.subtract(v_world_target, v_world_robot);
		d = LA.norm(v_robot_target);
		return d;

	# returns the target angle and distance to go til goal is met
	def calculateStep(self, target_pose):
		t_q = calculateAngle(target_pose);
		t_d = calculateDistToGo(target_pose);
		pass;

def main():
	tf_world_cam = rp.RobotPose(CONSTANTS.TF_TARGET_ORIENTATION, 
		CONSTANTS.TF_CAM_ROBOT_POSITION);
	ad = AutonomousDrive();
	print ad.targetPose.R;
	tf_world_robot = ad.calculateTfWorldToRobot(tf_world_cam.tf, math.pi/4);
	print tf_world_robot;
	print ad.calculateDistToGo(tf_world_cam.tf, 0);

if __name__ == '__main__':
	main();