using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            MessageParser m = new MessageParser();  
            String message1 = "<1:v:10000>|<2:v:8000>|<3:v:6000>|<4:v:3575>|<5:v:2000>";
            ArrayList data = m.parseMessage(message1);
            Console.WriteLine("Hello");
        }
    }
}
