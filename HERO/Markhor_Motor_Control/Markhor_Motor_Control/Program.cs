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

namespace Markhor_Motor_Control
{
    public class Program
    {
        static CTRE.TalonSrx leftDriveMotor = new CTRE.TalonSrx(1);
        static CTRE.TalonSrx rightDrive = new CTRE.TalonSrx(2);
        static CTRE.TalonSrx scoopsMotor = new CTRE.TalonSrx(3);
        static CTRE.TalonSrx depthMotor = new CTRE.TalonSrx(4);
        static CTRE.TalonSrx winchMotor  = new CTRE.TalonSrx(5);


        /** Serial object, this is constructed on the serial number. */
        static System.IO.Ports.SerialPort uart;
        /** Ring buffer holding the bytes to transmit. */
        static byte[] tx = new byte[1024];
        static int txIn = 0;
        static int txOut = 0;
        static int txCnt = 0;
        /** Cache for reading out bytes in serial driver. */
        static byte[] rx = new byte[1024];
        /* initial message to send to the terminal */
        static byte[] initMessage = MakeByteArrayFromString("System has been initialized.\r\n");
        /** @return the maximum number of bytes we can read*/
        private static int CalcRemainingCap()
        {
            /* firs calc the remaining capacity in the ring buffer */
            int rem = tx.Length - txCnt;
            /* cap the return to the maximum capacity of the rx array */
            if (rem > rx.Length)
                rem = rx.Length;
            return rem;
        }
        /** @param received byte to push into ring buffer */
        private static void PushByte(byte datum)
        {
            tx[txIn] = datum;
            if (++txIn >= tx.Length)
                txIn = 0;
            ++txCnt;
        }
        /** 
         * Pop the oldest byte out of the ring buffer.
         * Caller must ensure there is at least one byte to pop out by checking _txCnt.
         * @return the oldest byte in buffer.
         */
        private static byte PopByte()
        {
            byte retval = tx[txOut];
            if (++txOut >= tx.Length)
                txOut = 0;
            --txCnt;
            return retval;
        }
        /** entry point of the application */
        public static void Main()
        {
            ArrayList motorData = new ArrayList();
            uart = new System.IO.Ports.SerialPort(CTRE.HERO.IO.Port1.UART, 115200);
            uart.Open();
            /* send a message to the terminal for the user to see */
            uart.Write(initMessage, 0, initMessage.Length);
            /* loop forever */
            while (true)
            {
                /* read bytes out of uart */
                if (uart.BytesToRead > 0)
                {
                    int readCnt = uart.Read(rx, 0, CalcRemainingCap());
                    for (int i = 0; i < readCnt; ++i)
                    {
                        PushByte(rx[i]);
                    }
                }

                byte[] outboundMessage = MakeByteArrayFromString(makeOutboundMessage(motorData));
                if (uart.CanWrite)
                {
                    uart.Write(outboundMessage, 0, outboundMessage.Length);
                }
                /* wait a bit, keep the main loop time constant, this way you can add to this example (motor control for example). */
                System.Threading.Thread.Sleep(10);
            }
        }

        private static byte[] MakeByteArrayFromString(String msg)
        {
            byte[] retval = new byte[msg.Length];
            for (int i = 0; i < msg.Length; ++i)
                retval[i] = (byte)msg[i];
            return retval;
        }

        private static String MakeStringFromByteArray(byte[] data)
        {
            String retval = "";
            for(int i = 0; i < data.Length; i++)
            {
                retval += data[i].ToString();
            }
            return retval;
        }

        private static String makeOutboundMessage(ArrayList controlData)
        {
            String outboundMessage = "";
            for(int i = 0; i < controlData.Count; i++)
            {
                outboundMessage += ((ControlData)controlData[i]).getWriteableMessageString();
                outboundMessage += (i < controlData.Count - 1) ? "|" : "";
            }
            return outboundMessage;
        }
    }
}
