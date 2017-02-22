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
            ArrayList controlData = new ArrayList();

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
                            char mode = (subparts[1]).ToCharArray()[0];
                            int setpoint = Int32.Parse(subparts[2]);
                            controlData.Add(new SetpointData(deviceID, mode, setpoint));
                        }
                    }
                    catch { /* malformed message, dont try to add this one */ }
                }

            }
            catch
            {
                return new ArrayList();
            }

            return controlData;
        }
    }
}

