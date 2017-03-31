package common;

import static org.junit.Assert.*;

import org.junit.Test;

import net.java.games.input.Controller;
import net.java.games.input.ControllerEnvironment;

public class JoystickTest {

	@Test
	public void test() throws InterruptedException 
	{
		Controller[] ca = ControllerEnvironment.getDefaultEnvironment().getControllers();

        for(int i =0;i<ca.length;i++){

            /* Get the name of the controller */
            System.out.println(ca[i].getName());
            System.out.println("Type: "+ca[i].getType().toString());
        }
		
		Gamepad g = new Gamepad();
		while(true)
		{
			g.update();
			//System.out.println(g.getButtonA() + ":" +  g.getButtonB()  + ":" + g.getButtonX() + ":" + g.getButtonY() +
			//			 ":" + g.getButtonLB() + ":" + g.getButtonRB() + ":" + g.getButtonBack() + ":" + g.getButtonStart() +
			//			 ":" + g.getButtonLJ() + ":" + g.getButtonRJ());
			
			System.out.println(g.getAxisX1() + ":" + g.getAxisY1() + ":" + g.getAxisX2() + ":" + g.getAxisY2() + ":" + g.getAxisT());
			//System.out.println(g.getDPad());
			Thread.sleep(20);
		}
	}
}
