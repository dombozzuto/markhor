package network;

import java.io.*;
import java.net.Socket;

import common.MessageQueue;
import gui.RobotData;

class RequestHandler extends Thread
{
    private Socket socket;
    private MessageQueue queue;
    
    RequestHandler( Socket socket , MessageQueue queue)
    {
        this.socket = socket;
        this.queue = queue;
    }

    @Override
    public void run()
    {
        try
        {
		   // Get input and output streams
		   BufferedReader in = new BufferedReader( new InputStreamReader( socket.getInputStream() ) );
		   PrintWriter out = new PrintWriter( socket.getOutputStream() );
		    
		   BufferedReader inFromClient = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		   String inboundMessageStr;
		   
		   try
		   {
			   inboundMessageStr = inFromClient.readLine();
			   if(inboundMessageStr != null && inboundMessageStr.replace("\n\t ", "").equals("Finished"))
			   {
			       	if(!queue.isEmpty())
			   		{
			       		queue.pop();
			   		}
				} 
		   }
		   catch(Exception e)
		   {
			   e.printStackTrace();
			   inboundMessageStr = "Errors";
		   }
		   
		
		    System.out.println("Received: " + inboundMessageStr);
		    RobotData.setMostRecentMessage(inboundMessageStr);
		    
		    if(!queue.isEmpty())
		    {
		    	queue.peek();
		    	out.println(queue.peek().getMessageString());
		    	System.out.println("Sent: " + queue.peek().getMessageString());
		        out.flush();
		    }
		    else
		    {
		    	out.println("<0|-1>");
		    	out.flush();
		    }
		    
		    // Close our connection
		    in.close();
		    out.close();
		    socket.close();
		        }
		        catch( Exception e )
		        {
		            e.printStackTrace();
		        }
		    }
}