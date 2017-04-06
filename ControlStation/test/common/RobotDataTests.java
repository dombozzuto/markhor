package common;
import static org.junit.Assert.*;

import org.junit.Test;

import common.MotorMode;
import gui.RobotData;

public class RobotDataTests {

	@Test
	public void regexMatchesAndUpdates() 
	{
		String messageString = "<0.0,1.0,3.0,3.0,4.3>,<0.5,0.4,0.3,0.2,0.1>,<1.0,2.0,3.0,4.0,5.0>,<0,1,2,3,4>,<0,1,0,1>";
		RobotData.getInstance().updateValuesFromString(messageString);
		assertEquals(0.0, RobotData.getInstance().getLeftMotorSetpoint(), 0.1);
		assertEquals(1.0, RobotData.getInstance().getRightMotorSetpoint(), 0.1);
		assertEquals(3.0, RobotData.getInstance().getScoopMotorSetpoint(), 0.1);
		assertEquals(3.0, RobotData.getInstance().getDepthMotorSetpoint(), 0.1);
		assertEquals(4.3, RobotData.getInstance().getWinchMotorSetpoint(), 0.1);
		
		assertEquals(0.5, RobotData.getInstance().getLeftMotorActual(), 0.1);
		assertEquals(0.4, RobotData.getInstance().getRightMotorActual(), 0.1);
		assertEquals(0.3, RobotData.getInstance().getScoopMotorActual(), 0.1);
		assertEquals(0.2, RobotData.getInstance().getDepthMotorActual(), 0.1);
		assertEquals(0.1, RobotData.getInstance().getWinchMotorActual(), 0.1);
		
		assertEquals(1.0, RobotData.getInstance().getLeftMotorCurrent(), 0.1);
		assertEquals(2.0, RobotData.getInstance().getRightMotorCurrent(), 0.1);
		assertEquals(3.0, RobotData.getInstance().getScoopMotorCurrent(), 0.1);
		assertEquals(4.0, RobotData.getInstance().getDepthMotorCurrent(), 0.1);
		assertEquals(5.0, RobotData.getInstance().getWinchMotorCurrent(), 0.1);
		
		assertEquals(MotorMode.K_PERCENT_VBUS, RobotData.getInstance().getLeftMotorMode());
		assertEquals(MotorMode.K_CURRENT, RobotData.getInstance().getRightMotorMode());
		assertEquals(MotorMode.K_SPEED, RobotData.getInstance().getScoopMotorMode());
		assertEquals(MotorMode.K_POSITION, RobotData.getInstance().getDepthMotorMode());
		assertEquals(MotorMode.K_VOLTAGE, RobotData.getInstance().getWinchMotorMode());
		
		assertFalse(RobotData.getInstance().isDepthMotorUpperLimit());
		assertTrue(RobotData.getInstance().isDepthMotorLowerLimit());
		assertFalse(RobotData.getInstance().isWinchMotorUpperLimit());
		assertTrue(RobotData.getInstance().isWinchMotorLowerLimit());
		
		
		
	}

}
