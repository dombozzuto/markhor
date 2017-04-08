package gui;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import common.MotorMode;
import data.Motor;

public class NewRobotDataToBeRenamed 
{
	private static String messageString = "";
	
	private Motor leftMotor;
	private Motor rightMotor;
	private Motor scoopMotor;
	private Motor depthMotor;
	private Motor winchMotor;
	
	private static NewRobotDataToBeRenamed instance = new NewRobotDataToBeRenamed();
	
	public static NewRobotDataToBeRenamed getInstance()
	{
		return instance;
	}
	
	public static void setMostRecentMessage(String msgStr)
	{
		messageString = msgStr;
	}
	
	public Motor getLeftMotor() {return leftMotor;}
	public Motor getRightMotor() {return rightMotor;}
	public Motor getScoopMotor() {return scoopMotor;}
	public Motor getDepthMotor() {return depthMotor;}
	public Motor getWinchMotor() {return winchMotor;}
	
	
	
}
