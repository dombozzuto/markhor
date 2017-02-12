using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections;
using Microsoft.SPOT;


namespace Markhor_Motor_Control
{
    class MessageParser
    {

        public MessageParser()
        {

        }

        public ArrayList parseMessage(String msg)
        {
            ArrayList controlData = new ArrayList();

            string[] msg_parts = msg.Split('|');
        

            return controlData;
        }


    }
}
