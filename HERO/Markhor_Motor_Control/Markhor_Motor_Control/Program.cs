/**
 * Example HERO application can reads a serial port and echos the bytes back.
 * After deploying this application, the user can open a serial terminal and type while the HERO echoes the typed keys back.
 * Use a USB to UART (TTL) cable like the Adafruit Raspberry PI or FTDI-TTL cable.
 * Use device manager to figure out which serial port number to select in your PC terminal program.
 * HERO Gadgeteer Port 1 is used in this example, but can be changed at the top of Main().
 */
using System;
using System.Threading;
using Microsoft.SPOT;
using System.Collections;
using System.Text.RegularExpressions;

namespace Markhor_Motor_Control
{
    public class Program
    {
        

        static System.IO.Ports.SerialPort uart;
        static byte[] rx = new byte[1024];

        public static void Main()
        {
            CTRE.TalonSrx leftMotor = new CTRE.TalonSrx(1);
            CTRE.TalonSrx rightMotor = new CTRE.TalonSrx(2);
            CTRE.TalonSrx scoopMotor = new CTRE.TalonSrx(3);
            CTRE.TalonSrx depthMotor = new CTRE.TalonSrx(4);
            CTRE.TalonSrx winchMotor = new CTRE.TalonSrx(5);

            ArrayList motorSetpointData = new ArrayList();
            ArrayList motorStatusData = new ArrayList();
            ArrayList talons = new ArrayList();

            talons.Add(leftMotor);
            talons.Add(rightMotor);
            talons.Add(scoopMotor);
            talons.Add(depthMotor);
            talons.Add(winchMotor);

            String inboundMessageStr = "";
            String outboundMessageStr = "";

            SetpointData leftMotorSetpointData = new SetpointData(1, 'v', 5000);
            SetpointData rightMotorSetpointData = new SetpointData(2, 'v', 5000);
            SetpointData scoopMotorSetpointData = new SetpointData(3, 'v', 5000);
            SetpointData depthMotorSetpointData = new SetpointData(4, 'v', 5000);
            SetpointData winchMotorSetpointData = new SetpointData(5, 'v', 5000);

            StatusData leftMotorStatusData = new StatusData(1, leftMotor);
            StatusData rightMotorStatusData = new StatusData(2, rightMotor);
            StatusData scoopMotorStatusData = new StatusData(3, scoopMotor);
            StatusData depthMotorStatusData = new StatusData(4, depthMotor);
            StatusData winchMotorStatusData = new StatusData(5, winchMotor);

            motorSetpointData.Add(leftMotorSetpointData);
            motorSetpointData.Add(rightMotorSetpointData);
            motorSetpointData.Add(scoopMotorSetpointData);
            motorSetpointData.Add(depthMotorSetpointData);
            motorSetpointData.Add(winchMotorSetpointData);

            motorStatusData.Add(leftMotorStatusData);
            motorStatusData.Add(rightMotorStatusData);
            motorStatusData.Add(scoopMotorStatusData);
            motorStatusData.Add(depthMotorStatusData);
            motorStatusData.Add(winchMotorStatusData);

            uart = new System.IO.Ports.SerialPort(CTRE.HERO.IO.Port1.UART, 115200);
            uart.Open();
            

            while (true)
            {
                //read whatever is available from the UART into the inboundMessageStr
                motorSetpointData = readUART(ref inboundMessageStr);

                //attempt to process whatever was contained in the most recent message
                processInboundData(motorSetpointData, talons);

                //get a bunch of data from the motors in their current states
                updateMotorStatusData(motorStatusData);

                //package that motor data into a formatted message
                outboundMessageStr = makeOutboundMessage(motorStatusData);

                //send that message back to the main CPU
                writeUART(outboundMessageStr);

                CTRE.Watchdog.Feed();
                //keep the loop timing consistent //TODO: evaluate if this is necessary
                //System.Threading.Thread.Sleep(10);
            }
        }

        private static ArrayList readUART(ref String messageStr)
        {
            ArrayList setpointData = new ArrayList();
            if (uart.BytesToRead > 0)
            {      
                int readCnt = uart.Read(rx, 0, 1024);
                for (int i = 0; i < readCnt; ++i)
                {
                    messageStr += (char)rx[i];
                    if ((char)rx[i] == '\n')
                    {
                        setpointData = MessageParser.parseMessage(messageStr);
                        messageStr = "";
                    }
                }
            }
            return setpointData;
        }

        private static void writeUART(String messageStr)
        {
            byte[] outboundMessage = MakeByteArrayFromString(messageStr);
            if (uart.CanWrite)
            {
                uart.Write(outboundMessage, 0, outboundMessage.Length);
            }
        }

        private static byte[] MakeByteArrayFromString(String msg)
        {
            byte[] retval = new byte[msg.Length];
            for (int i = 0; i < msg.Length; ++i)
                retval[i] = (byte)msg[i];
            return retval;
        }

        private static void updateMotorStatusData(ArrayList statusData)
        {
            for(int i = 0; i < statusData.Count; i++)
            {
                ((StatusData)statusData[i]).updateStatusData();
            }
        }

        private static String makeOutboundMessage(ArrayList statusData)
        {
            String outboundMessage = "";
            for(int i = 0; i < statusData.Count; i++)
            {
                outboundMessage += ((StatusData)statusData[i]).getOutboundMessage();
            }
            outboundMessage += "\n\r";
            return outboundMessage;
        }

        private static void processInboundData(ArrayList setpointDataList, ArrayList talons)
        {
            for(int i = 0; i < setpointDataList.Count; i++)
            {
                SetpointData setpointData = (SetpointData)setpointDataList[i];
                //((CTRE.TalonSrx)talons[i]).SetControlMode(setpointData.getMode());
                ((CTRE.TalonSrx)talons[i]).Set(setpointData.getConvertedSetpoint());
            }
            

        }
    }  
}
