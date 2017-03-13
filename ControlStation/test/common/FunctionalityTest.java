package common;

import messages.*;
import network.NetworkServer;

public class FunctionalityTest 
{
	public static void main(String [] args)
	{
		final int port = 11000;
		
		MessageQueue mq = new MessageQueue();
		NetworkServer server = new NetworkServer(port);

		mq.add(new MsgDriveTime(5.0, 0.75));
		mq.add(new MsgDriveTime(10.0, 1.00));
		mq.add(new MsgDriveTime(5.0, -0.50));
		mq.add(new MsgStop());
		
		
		server.startServer();
		try
        {
            Thread.sleep( 60000 );
        }
        catch( Exception e )
        {
            e.printStackTrace();
        }

        server.stopServer();
	}
}
