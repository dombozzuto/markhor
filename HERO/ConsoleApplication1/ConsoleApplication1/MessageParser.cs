using System;
using System.Collections;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication1
{
    class MessageParser
    {
        public MessageParser()
        {

        }

        public ArrayList parseMessage(String msg)
        {
            ArrayList controlData = new ArrayList();

            try
            {
                String[] msg_parts = msg.Split('|');
                Console.WriteLine("{0} parts in the message", msg_parts.Length);
                //msg format: <DEVICE_ID:MODE:SETPOINT>
                String regex_pattern = @"<(\d+):([vs]):(\d+)>";
                foreach(String part in msg_parts)
                {
                    foreach(Match m in Regex.Matches(part, regex_pattern))
                    {
                        int deviceID = Int32.Parse(m.Groups[1].Value);
                        char mode = Char.Parse(m.Groups[2].Value);
                        int setpoint = Int32.Parse(m.Groups[3].Value);
                        controlData.Add(new ControlData(deviceID, mode, setpoint));
                    }
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

