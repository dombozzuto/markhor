using System;
using System.Threading;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;

namespace Markhor_Motor_Control
{
    public class Program
    {

        static System.IO.Ports.SerialPort uart;

        static CTRE.TalonSrx leftDriveMotor = new CTRE.TalonSrx(1);
        static CTRE.TalonSrx rightDriveMotor = new CTRE.TalonSrx(2);
        static CTRE.TalonSrx scoopMotor = new CTRE.TalonSrx(3);
        static CTRE.TalonSrx depthMotor = new CTRE.TalonSrx(4);
        static CTRE.TalonSrx winchMotor = new CTRE.TalonSrx(5);



        private void parseMessage()
        {

        }


        public static void Main()
        {
            /* simple counter to print and watch using the debugger */
            int counter = 0;
            /* loop forever */
            while (true)
            {
                /* print the three analog inputs as three columns */
                Debug.Print("Counter Value: " + counter);

                /* increment counter */
                ++counter; /* try to land a breakpoint here and hover over 'counter' to see it's current value.  Or add it to the Watch Tab */

                /* wait a bit */
                System.Threading.Thread.Sleep(100);
            }
        }
    }
}
