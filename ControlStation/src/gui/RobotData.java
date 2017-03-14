package gui;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import common.MotorMode;

public class RobotData 
{
	private double leftMotorSetpoint = 0.0;
	private double rightMotorSetpoint = 0.0;
	private double scoopMotorSetpoint = 0.0;
	private double depthMotorSetpoint = 0.0;
	private double winchMotorSetpoint = 0.0;
	
	private double leftMotorActual = 0.0;
	private double rightMotorActual = 0.0;
	private double scoopMotorActual = 0.0;
	private double depthMotorActual = 0.0;
	private double winchMotorActual = 0.0;
	
	private double leftMotorCurrent = 0.0;
	private double rightMotorCurrent = 0.0;
	private double scoopMotorCurrent = 0.0;
	private double depthMotorCurrent = 0.0;
	private double winchMotorCurrent = 0.0;
	
	private MotorMode leftMotorMode = MotorMode.K_PERCENT_VBUS;
	private MotorMode rightMotorMode = MotorMode.K_PERCENT_VBUS;
	private MotorMode scoopMotorMode = MotorMode.K_PERCENT_VBUS;
	private MotorMode depthMotorMode = MotorMode.K_PERCENT_VBUS;
	private MotorMode winchMotorMode = MotorMode.K_PERCENT_VBUS;
	
	private boolean depthMotorUpperLimit = false;
	private boolean depthMotorLowerLimit = false;
	private boolean winchMotorUpperLimit = false;
	private boolean winchMotorLowerLimit = false;
	
	private static RobotData instance = new RobotData();
	
	public static RobotData getInstance()
	{
		return instance;
	}
	
	public void updateValuesFromString(String messageString)
	{
		final String patternStr = "(<.*>),(<.*>),(<.*>),(<.*>),(<.*>)";
		Pattern pattern = Pattern.compile(patternStr);
		Matcher m = pattern.matcher(messageString);
		if(m.matches())
		{
			String motorSetpoints = m.group(1);
			String motorActuals = m.group(2);
			String motorCurrents = m.group(3);
			String motorModes = m.group(4);
			String limitSwtiches = m.group(5);
			
			updateMotorSetpoints(motorSetpoints);
			updateMotorActuals(motorActuals);
			updateMotorCurrents(motorCurrents);
			updateMotorModes(motorModes);
			updateLimitSwitches(limitSwtiches);
		}
	}
	
	private void updateMotorSetpoints(String setpointString)
	{
		final String patternStr = "<(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+)>";
		Pattern pattern = Pattern.compile(patternStr);
		Matcher m = pattern.matcher(setpointString);
		if(m.matches())
		{
			leftMotorSetpoint = Double.parseDouble(m.group(1));
			rightMotorSetpoint = Double.parseDouble(m.group(2));
			scoopMotorSetpoint = Double.parseDouble(m.group(3));
			depthMotorSetpoint = Double.parseDouble(m.group(4));
			winchMotorSetpoint = Double.parseDouble(m.group(5));
		}
		else
		{
			System.out.println("Update Setpoints Failed!");
		}
	}
	
	private void updateMotorActuals(String actualString)
	{
		final String patternStr = "<(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+)>";
		Pattern pattern = Pattern.compile(patternStr);
		Matcher m = pattern.matcher(actualString);
		if(m.matches())
		{
			leftMotorActual = Double.parseDouble(m.group(1));
			rightMotorActual = Double.parseDouble(m.group(2));
			scoopMotorActual = Double.parseDouble(m.group(3));
			depthMotorActual = Double.parseDouble(m.group(4));
			winchMotorActual = Double.parseDouble(m.group(5));
		}
		else
		{
			System.out.println("Update Actuals Failed!");
		}
	}
	
	private void updateMotorCurrents(String currentString)
	{
		final String patternStr = "<(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+),(\\d+\\.\\d+)>";
		Pattern pattern = Pattern.compile(patternStr);
		Matcher m = pattern.matcher(currentString);
		if(m.matches())
		{
			leftMotorCurrent = Double.parseDouble(m.group(1));
			rightMotorCurrent = Double.parseDouble(m.group(2));
			scoopMotorCurrent = Double.parseDouble(m.group(3));
			depthMotorCurrent = Double.parseDouble(m.group(4));
			winchMotorCurrent = Double.parseDouble(m.group(5));
		}
		else
		{
			System.out.println("Update Currents Failed!");
		}
	}
	
	private void updateMotorModes(String modeString)
	{
		final String patternStr = "<(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)>";
		Pattern pattern = Pattern.compile(patternStr);
		Matcher m = pattern.matcher(modeString);
		if(m.matches())
		{
			try
			{
				leftMotorMode = MotorMode.values()[Integer.parseInt(m.group(1))];
				rightMotorMode = MotorMode.values()[Integer.parseInt(m.group(2))];
				scoopMotorMode = MotorMode.values()[Integer.parseInt(m.group(3))];
				depthMotorMode = MotorMode.values()[Integer.parseInt(m.group(4))];
				winchMotorMode = MotorMode.values()[Integer.parseInt(m.group(5))];		
			}
			catch(Exception e)
			{
				System.out.println("Update Modes Failed!");
			}
		}
		else
		{
			System.out.println("Update Modes Failed!");
		}
	}
	
	private void updateLimitSwitches(String limitString)
	{
		final String patternStr = "<(0|1),(0|1),(0|1),(0|1)>";
		Pattern pattern = Pattern.compile(patternStr);
		Matcher m = pattern.matcher(limitString);
		if(m.matches())
		{
			depthMotorUpperLimit = Integer.parseInt(m.group(1)) == 1 ? true : false;
			depthMotorLowerLimit = Integer.parseInt(m.group(2)) == 1 ? true : false;
			winchMotorUpperLimit = Integer.parseInt(m.group(3)) == 1 ? true : false;
			winchMotorLowerLimit = Integer.parseInt(m.group(4)) == 1 ? true : false;
		}
		else
		{
			System.out.println("Update Limits Failed!");
		}
	}
	
	
	
	public double getLeftMotorSetpoint() {
		return leftMotorSetpoint;
	}

	public double getRightMotorSetpoint() {
		return rightMotorSetpoint;
	}

	public double getScoopMotorSetpoint() {
		return scoopMotorSetpoint;
	}

	public double getDepthMotorSetpoint() {
		return depthMotorSetpoint;
	}

	public double getWinchMotorSetpoint() {
		return winchMotorSetpoint;
	}

	public double getLeftMotorActual() {
		return leftMotorActual;
	}

	public double getRightMotorActual() {
		return rightMotorActual;
	}

	public double getScoopMotorActual() {
		return scoopMotorActual;
	}

	public double getDepthMotorActual() {
		return depthMotorActual;
	}

	public double getWinchMotorActual() {
		return winchMotorActual;
	}

	public double getLeftMotorCurrent() {
		return leftMotorCurrent;
	}

	public double getRightMotorCurrent() {
		return rightMotorCurrent;
	}

	public double getScoopMotorCurrent() {
		return scoopMotorCurrent;
	}

	public double getDepthMotorCurrent() {
		return depthMotorCurrent;
	}

	public double getWinchMotorCurrent() {
		return winchMotorCurrent;
	}

	public MotorMode getLeftMotorMode() {
		return leftMotorMode;
	}

	public MotorMode getRightMotorMode() {
		return rightMotorMode;
	}

	public MotorMode getScoopMotorMode() {
		return scoopMotorMode;
	}

	public MotorMode getDepthMotorMode() {
		return depthMotorMode;
	}

	public MotorMode getWinchMotorMode() {
		return winchMotorMode;
	}

	public boolean isDepthMotorUpperLimit() {
		return depthMotorUpperLimit;
	}

	public boolean isDepthMotorLowerLimit() {
		return depthMotorLowerLimit;
	}

	public boolean isWinchMotorUpperLimit() {
		return winchMotorUpperLimit;
	}

	public boolean isWinchMotorLowerLimit() {
		return winchMotorLowerLimit;
	}

	private RobotData() {}
	


	

	
	
	
}
