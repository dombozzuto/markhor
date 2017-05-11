using System;
using Microsoft.SPOT;
using System;
using System.Collections;
using System.Text.RegularExpressions;

namespace Markhor_Motor_Control
{
    class MessageParser
    {
        public MessageParser()
        {

        }

        public static ArrayList parseMessage(String msg)
        {
            long start_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
            ArrayList controlData = new ArrayList();
            String pattern = @"<([0-9]+):([0-9]+):([-0-9]+\.[0-9]+)>";
            MatchCollection mc = Regex.Matches(msg, pattern);
            long match_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;

            foreach (Match m in mc)
            {
                String data = m.Value;
                data = data.Substring(1, data.Length - 2);
                String[] subparts = data.Split(':');
                int deviceID = Int32.Parse(subparts[0]);
                int mode = Int32.Parse(subparts[1]);
                Double setpoint = Double.Parse(subparts[2]);
                controlData.Add(new SetpointData(deviceID, mode, setpoint));
            }
            long finish_time = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
            Debug.Print("\tParse Time:" + (finish_time - start_time).ToString());
            Debug.Print("\t\tMatch Time:" + (match_time - start_time).ToString());


            /*
            try
            {
                String[] msg_parts = msg.Split('|');
                //msg format: <DEVICE_ID:MODE:SETPOINT>
                foreach (String part in msg_parts)
                {
                    try
                    {
                        //check the end delimiters for the full message
                        if (part[0].Equals('<') && part[part.Length - 1].Equals('>'))
                        {
                            String[] subparts = part.Split(':');
                            int deviceID = Int32.Parse(subparts[0]);
                            int mode = Int32.Parse(subparts[1]);
                            int setpoint = Int32.Parse(subparts[2]);
                            controlData.Add(new SetpointData(deviceID, mode, setpoint));
                        }
                    }
                    catch { }
                }

            }
            catch
            {
                return new ArrayList();
            }
            */

            return controlData;
        }

        public static ArrayList parseMessage2(byte[] message)
        {
            ArrayList controlData = new ArrayList();
            if (message.Length < 34) //check message size
                return null;
            if (message[0] != 0xDE || message[1] != 0xAD) //check start bytes == DEAD
                return null;
            if (message[32] != 0xBE || message[33] != 0xEF) //check end bytes == BEEF
                return null;

            for (int i = 0; i < 5; i++)
            {
                int devID = message[i * 6 + 2];
                int mode = message[i * 6 + 3];
                byte[] floatbytes = new byte[] { message[i * 6 + 4], message[i * 6 + 5], message[i * 6 + 6], message[i * 6 + 7] };
                float setpoint = BitConverter.ToSingle(floatbytes, 0);
                controlData.Add(new Markhor_Motor_Control.SetpointData(devID, mode, setpoint));
            }
            return controlData;
        }

    }

    
}

