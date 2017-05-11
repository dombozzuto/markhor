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
using System.Text;

namespace Markhor_Motor_Control
{


    public class Program
    {
        public static long count = 0;

        private const int RESET_DRIVE_ENC = 0;
        private const int RESET_DEPTH_ENC = 1;
        private const int RESET_SCOOP_ENC = 2;
        private const int RESET_WINCH_ENC = 3;

        private const int LDRIVE_ID = 0;
        private const int RDRIVE_ID = 1;
        private const int SCOOP_ID = 2;
        private const int DEPTH_ID = 3;
        private const int WINCH_ID = 4;
        //private const int SCOOP2_ID = 5;

        static bool [] flags = { false, false, false, false };

        static System.IO.Ports.SerialPort uart;
        static byte[] rx = new byte[1024];

        public static void Main()
        {
            CTRE.TalonSrx leftMotor = new CTRE.TalonSrx(1);
            CTRE.TalonSrx rightMotor = new CTRE.TalonSrx(2);
            CTRE.TalonSrx scoopMotor = new CTRE.TalonSrx(3);
            CTRE.TalonSrx depthMotor = new CTRE.TalonSrx(4);
            CTRE.TalonSrx winchMotor = new CTRE.TalonSrx(5);
            //CTRE.TalonSrx scoopMotor2 = new CTRE.TalonSrx(6);

            leftMotor.SetFeedbackDevice(CTRE.TalonSrx.FeedbackDevice.QuadEncoder);
            rightMotor.SetFeedbackDevice(CTRE.TalonSrx.FeedbackDevice.QuadEncoder);
            scoopMotor.SetFeedbackDevice(CTRE.TalonSrx.FeedbackDevice.QuadEncoder);
            depthMotor.SetFeedbackDevice(CTRE.TalonSrx.FeedbackDevice.CtreMagEncoder_Absolute);
            winchMotor.SetFeedbackDevice(CTRE.TalonSrx.FeedbackDevice.QuadEncoder);
            //scoopMotor2.SetFeedbackDevice(CTRE.TalonSrx.FeedbackDevice.QuadEncoder);

            leftMotor.SetSensorDirection(false);
            rightMotor.SetSensorDirection(true);
            scoopMotor.SetSensorDirection(false);
            depthMotor.SetSensorDirection(false);
            winchMotor.SetSensorDirection(false);
            //scoopMotor2.SetSensorDirection(false);

            leftMotor.ConfigEncoderCodesPerRev(80);
            rightMotor.ConfigEncoderCodesPerRev(80);
            scoopMotor.ConfigEncoderCodesPerRev(80);
            depthMotor.ConfigEncoderCodesPerRev(80);
            winchMotor.ConfigEncoderCodesPerRev(80);
            //scoopMotor2.ConfigEncoderCodesPerRev(80);

            leftMotor.SetP(0, 0.35F);
            leftMotor.SetI(0, 0.0F);
            leftMotor.SetD(0, 0.0F);
            leftMotor.SetF(0, 0.0F);
            leftMotor.SelectProfileSlot(0);

            rightMotor.SetP(0, 0.35F);
            rightMotor.SetI(0, 0.0F);
            rightMotor.SetD(0, 0.0F);
            rightMotor.SetF(0, 0.0F);
            rightMotor.SelectProfileSlot(0);

            scoopMotor.SetP(0, 0.6F);
            scoopMotor.SetI(0, 0.0F);
            scoopMotor.SetD(0, 0.0F);
            scoopMotor.SetF(0, 0.0F);
            scoopMotor.SelectProfileSlot(0);

            depthMotor.SetP(0, 4.0F);
            depthMotor.SetI(0, 0.0F);
            depthMotor.SetD(0, 0.0F);
            depthMotor.SetF(0, 0.0F);
            depthMotor.SelectProfileSlot(0);

            winchMotor.SetP(0, 0.6F);
            winchMotor.SetI(0, 0.0F);
            winchMotor.SetD(0, 0.0F);
            winchMotor.SetF(0, 0.0F);
            winchMotor.SelectProfileSlot(0);

            //scoopMotor2.SetP(0, 0.6F);
            //scoopMotor2.SetI(0, 0.0F);
            //scoopMotor2.SetD(0, 0.0F);
            //scoopMotor2.SetF(0, 0.0F);
            //scoopMotor2.SelectProfileSlot(0);

            leftMotor.ConfigNominalOutputVoltage(+0.0F, -0.0F);
            rightMotor.ConfigNominalOutputVoltage(+0.0F, -0.0F);
            scoopMotor.ConfigNominalOutputVoltage(+0.0F, -0.0F);
            depthMotor.ConfigNominalOutputVoltage(+0.0F, -0.0F);
            winchMotor.ConfigNominalOutputVoltage(+0.0F, -0.0F);
            //scoopMotor2.ConfigNominalOutputVoltage(+0.0F, -0.0F);

            leftMotor.SetAllowableClosedLoopErr(0, 0);
            rightMotor.SetAllowableClosedLoopErr(0, 0);
            scoopMotor.SetAllowableClosedLoopErr(0, 0);
            depthMotor.SetAllowableClosedLoopErr(0, 0);
            winchMotor.SetAllowableClosedLoopErr(0, 0);
            //scoopMotor2.SetAllowableClosedLoopErr(0, 0);

            leftMotor.SetPosition(0);
            rightMotor.SetPosition(0);
            scoopMotor.SetPosition(0);
            depthMotor.SetPosition(0);
            winchMotor.SetPosition(0);
            //scoopMotor2.SetPosition(0);

            leftMotor.SetVoltageRampRate(0);
            rightMotor.SetVoltageRampRate(0);
            scoopMotor.SetVoltageRampRate(0);
            depthMotor.SetVoltageRampRate(0);
            winchMotor.SetVoltageRampRate(0);
            //scoopMotor2.SetVoltageRampRate(0);

            ArrayList motorSetpointData = new ArrayList();
            ArrayList motorStatusData = new ArrayList();
            ArrayList talons = new ArrayList();

            talons.Add(leftMotor);
            talons.Add(rightMotor);
            talons.Add(scoopMotor);
            talons.Add(depthMotor);
            talons.Add(winchMotor);
            //talons.Add(scoopMotor2);

            String inboundMessageStr = "";
            String outboundMessageStr = "";

            SetpointData leftMotorSetpointData = new SetpointData(1, 0, 0.0F);
            SetpointData rightMotorSetpointData = new SetpointData(2, 0, 0.0F);
            SetpointData scoopMotorSetpointData = new SetpointData(3, 0, 0.0F);
            SetpointData depthMotorSetpointData = new SetpointData(4, 0, 0.0F);
            SetpointData winchMotorSetpointData = new SetpointData(5, 0, 0.0F);
            //SetpointData scoopMotor2SetpointData = new SetpointData(6, 0, 0.0F);

            StatusData leftMotorStatusData = new StatusData(1, leftMotor);
            StatusData rightMotorStatusData = new StatusData(2, rightMotor);
            StatusData scoopMotorStatusData = new StatusData(3, scoopMotor);
            StatusData depthMotorStatusData = new StatusData(4, depthMotor);
            StatusData winchMotorStatusData = new StatusData(5, winchMotor);
            //StatusData scoopMotor2StatusData = new StatusData(6, scoopMotor2);

            motorSetpointData.Add(leftMotorSetpointData);
            motorSetpointData.Add(rightMotorSetpointData);
            motorSetpointData.Add(scoopMotorSetpointData);
            motorSetpointData.Add(depthMotorSetpointData);
            motorSetpointData.Add(winchMotorSetpointData);
            //motorSetpointData.Add(scoopMotor2SetpointData);

            motorStatusData.Add(leftMotorStatusData);
            motorStatusData.Add(rightMotorStatusData);
            motorStatusData.Add(scoopMotorStatusData);
            motorStatusData.Add(depthMotorStatusData);
            motorStatusData.Add(winchMotorStatusData);
            //motorStatusData.Add(scoopMotor2StatusData);

            CTRE.Watchdog.Feed();

            uart = new System.IO.Ports.SerialPort(CTRE.HERO.IO.Port1.UART, 115200);
            uart.Open();


            //CTRE.Gamepad gamepad = null;
            //Boolean isUsingGamepad = false;

            //try
            //{
            //    gamepad = new CTRE.Gamepad(CTRE.UsbHostDevice.GetInstance());
            //    isUsingGamepad = true;
            //}
            //catch (Exception e) {}
            

            if(false)
            {
                CTRE.Gamepad gamepad = new CTRE.Gamepad(CTRE.UsbHostDevice.GetInstance());
                while (true)
                {
                    /* drive robot using gamepad */

                    Drive(gamepad, leftMotor, rightMotor, scoopMotor, depthMotor, winchMotor);//, scoopMotor2);
                    /* feed watchdog to keep Talon's enabled if Gamepad is inserted. */
                    if (gamepad.GetConnectionStatus() == CTRE.UsbDeviceConnection.Connected)
                    {
                        CTRE.Watchdog.Feed();
                    }
                    /* run this task every 20ms */
                    Thread.Sleep(20);
                }
            }
            else
            {
                while(true)
                {
                    byte[] rx_copy = rx;
                    long start_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                    //read whatever is available from the UART into the inboundMessageStr
                    motorSetpointData = readUART2(ref inboundMessageStr);
//                    long read_uart_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                    CTRE.Watchdog.Feed();
                    //if any of the talon positions need to be reset, this will reset them
                    resetEncoderPositions(talons);
//                    long reset_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                    CTRE.Watchdog.Feed();
                    //attempt to process whatever was contained in the most recent message
                    processInboundData(motorSetpointData, talons);
//                    long process_inbound_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                    CTRE.Watchdog.Feed();
                    //get a bunch of data from the motors in their current states
                    updateMotorStatusData(motorStatusData);
//                    long update_status_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                    CTRE.Watchdog.Feed();
                    //package that motor data into a formatted message
                    outboundMessageStr = makeOutboundMessage(motorStatusData);
//                    long outbound_message_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                    CTRE.Watchdog.Feed();
                    //send that message back to the main CPU
                    writeUART(outboundMessageStr);
                    long write_uart_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;

                    //Debug.Print("set=" + winchMotor.GetSetpoint().ToString() + " mod=" + winchMotor.GetControlMode().ToString() +
                    //            "pos=" + winchMotor.GetPosition().ToString() + " vel=" + winchMotor.GetSpeed().ToString() + 
                    //            "err=" + winchMotor.GetClosedLoopError().ToString() + "vlt=" + winchMotor.GetOutputVoltage());
                    //Debug.Print(DateTime.Now.ToString());
                    CTRE.Watchdog.Feed();
                    //keep the loop timing consistent //TODO: evaluate if this is necessary
                    //System.Threading.Thread.Sleep(10);
//                    Debug.Print("Read UART Time:" + (read_uart_time - start_time).ToString());
//                    Debug.Print("Reset Time:" + (reset_time - read_uart_time).ToString());
//                    Debug.Print("Process Inbound Time:" + (process_inbound_time - reset_time).ToString());
//                    Debug.Print("Update Status Time:" + (update_status_time - process_inbound_time).ToString());
//                    Debug.Print("Make Outbound Time:" + (outbound_message_time - update_status_time).ToString());
//                    Debug.Print("Write UART Time:" + (write_uart_time - outbound_message_time).ToString());
                    Debug.Print("TOTAL Time:" + (write_uart_time - start_time).ToString());

                }
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
                        checkEncoderResetFlags(messageStr);
                        setpointData = MessageParser.parseMessage(messageStr);
                        messageStr = "";
                    }
                }
            }
            return setpointData;
        }

        private static ArrayList readUART2(ref String messageStr)
        {
            ArrayList setpointData = new ArrayList();
            if (uart.BytesToRead > 0)
            {
                int readCnt = uart.Read(rx, 0, 512);
                int i = 0;
                while(i < readCnt)
                {
                    //check start bytes
                    if( (rx[i] == 0xDE) && (rx[i+1] == 0xAD))
                    {
                        //check end bytes
                        if( (i + 30 < readCnt) && ( (rx[32+i] == 0xBE) && (rx[33+i] == 0xEF) ) )
                        {
                            byte[] newArray = new byte[34];
                            Array.Copy(rx, i, newArray, 0, newArray.Length);
                            setpointData = MessageParser.parseMessage2(newArray);
                            i = readCnt;
                        }
                    }
                    i++;
                }
            }
            return setpointData;
        }

        private static void resetEncoderPositions(ArrayList talons)
        {
            if(flags[RESET_DRIVE_ENC])
            {
                flags[RESET_DRIVE_ENC] = false;
                ((CTRE.TalonSrx)talons[LDRIVE_ID]).SetPosition(0.0F);
                ((CTRE.TalonSrx)talons[RDRIVE_ID]).SetPosition(0.0F);
                ((CTRE.TalonSrx)talons[LDRIVE_ID]).SetControlMode(CTRE.TalonSrx.
                    ControlMode.kPosition);
                ((CTRE.TalonSrx)talons[RDRIVE_ID]).SetControlMode(CTRE.TalonSrx.
                    ControlMode.kPosition);
                ((CTRE.TalonSrx)talons[LDRIVE_ID]).Set(0.0F);
                ((CTRE.TalonSrx)talons[RDRIVE_ID]).Set(0.0F);
            }
            if (flags[RESET_DEPTH_ENC])
            {
                flags[RESET_DEPTH_ENC] = false;
                ((CTRE.TalonSrx)talons[DEPTH_ID]).SetPosition(0.0F);
            }
            if (flags[RESET_SCOOP_ENC])
            {
                flags[RESET_SCOOP_ENC] = false;
                ((CTRE.TalonSrx)talons[SCOOP_ID]).SetPosition(0.0F);
            }
            if (flags[RESET_WINCH_ENC])
            {
                flags[RESET_WINCH_ENC] = false;
                ((CTRE.TalonSrx)talons[WINCH_ID]).SetPosition(0.0F);
            }
        }

        private static void checkEncoderResetFlags(String msg)
        {
            if(msg.Trim().Equals("<ResetDriveEncoders>"))
            {
                flags[RESET_DRIVE_ENC] = true;
            }
            if(msg.Trim().Equals("<ResetScoopEncoder>"))
            {
                flags[RESET_SCOOP_ENC] = true;
            }
            if(msg.Trim().Equals("<ResetDepthEncoder>"))
            {
                flags[RESET_DEPTH_ENC] = true;
            }
            if(msg.Trim().Equals("<ResetWinchEncoder>"))
            {
                flags[RESET_WINCH_ENC] = true;
            }
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
                float setpointVal = (float)(setpointData.getSetpoint());
                CTRE.TalonSrx talon = (CTRE.TalonSrx)talons[setpointData.getDeviceID() - 1];
                if(talon.GetControlMode() != setpointData.getMode())
                {
                    talon.SetControlMode(setpointData.getMode());
                    Debug.Print(setpointData.getMode().ToString());
                }
                if(talon.GetSetpoint() != setpointVal)
                {
                    talon.Set(setpointVal);
                    Debug.Print(setpointVal.ToString());
                }  
            }
        }

        static void Deadband(ref float value)
        {
            if (value < -0.050)
            {
                /* outside of deadband */
            }
            else if (value > +0.050)
            {
                /* outside of deadband */
            }
            else
            {
                /* within 10% so zero it */
                value = 0;
            }
        }
        static void Drive(CTRE.Gamepad gamepad,
            CTRE.TalonSrx leftMotor,
            CTRE.TalonSrx rightMotor,
            CTRE.TalonSrx scoopMotor,
            CTRE.TalonSrx depthMotor,
            CTRE.TalonSrx winchMotor)//,
            //CTRE.TalonSrx scoopMotor2)
        {
            depthMotor.SetControlMode(gamepad.GetButton(3) ? CTRE.TalonSrx.ControlMode.kPosition : CTRE.TalonSrx.ControlMode.kPercentVbus);
            float x = gamepad.GetAxis(0);
            float y = gamepad.GetAxis(1);

            float leftDriveSpeed = x+y;
            float rightDriveSpeed = x-y;
            //float leftScoopSpeed = 0.0F;
            //float rightScoopSpeed = 0.0F;
            //float winchSpeed = gamepad.GetAxis(5);
            float leftScoopSpeed = gamepad.GetAxis(5) / 1.5F;
            //float rightScoopSpeed = -leftScoopSpeed;
            float depthSpeed = gamepad.GetButton(0) ? 0.5F : 
                               gamepad.GetButton(2) ? -0.5F : 0.0F;
            float depthValue = gamepad.GetButton(0) ? 0.200F : (gamepad.GetButton(2) ? 0.00F : depthMotor.GetPosition());

            float winchSpeed = gamepad.GetButton(5) ? 1.0F :
                               gamepad.GetButton(6) ? -1.0F : 0.0F;
            float twist = gamepad.GetAxis(2);

            Deadband(ref leftDriveSpeed);
            Deadband(ref rightDriveSpeed);
            Deadband(ref leftScoopSpeed);
            //Deadband(ref rightScoopSpeed);
            Deadband(ref depthSpeed);
            Deadband(ref depthValue);
            Deadband(ref winchSpeed);

            StringBuilder stringbuilder = new StringBuilder();
            //            stringbuilder.Append(gamepad.GetAxis(0) + ":");
            //            stringbuilder.Append(gamepad.GetAxis(1) + ":");
            //            stringbuilder.Append(gamepad.GetAxis(2) + ":");
            //            stringbuilder.Append(gamepad.GetAxis(3) + ":");
            //            stringbuilder.Append(gamepad.GetAxis(4) + ":");
            //            stringbuilder.Append(gamepad.GetAxis(5) + "");
            stringbuilder.Append(count++ * 0.020F + ",");
            stringbuilder.Append(leftMotor.GetOutputCurrent() + ",");
            stringbuilder.Append(rightMotor.GetOutputCurrent());
            //stringbuilder.Append(depthMotor.GetPosition() + "  ");
            //stringbuilder.Append(winchMotor.GetOutputCurrent());
            //stringbuilder.Append(depthMotor.GetEncPosition());
            Debug.Print(stringbuilder.ToString());


            leftMotor.Set(leftDriveSpeed);
            rightMotor.Set(rightDriveSpeed);
            scoopMotor.Set(leftScoopSpeed);
            depthMotor.Set(gamepad.GetButton(3) ? depthValue : depthSpeed);
            winchMotor.Set(winchSpeed);
            //scoopMotor2.Set(rightScoopSpeed);

        }

    }  
}
