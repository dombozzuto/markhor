package common;

import messages.*;
import network.NetworkServer;

public class FunctionalityTest 
{
	public static void main(String [] args)
	{
		final int port = 11000;
		
		MessageQueue mq = new MessageQueue();
		NetworkServer server = new NetworkServer(port, mq);

		//mq.add(new MsgDriveTime(5.0, 0.75));
		//mq.add(new MsgDriveTime(10.0, 1.00));
		//mq.add(new MsgDriveTime(5.0, -0.50));
		//mq.add(new MsgScoopTime(4.0, 0.20));
		//mq.add(new MsgDepthTime(6.0, 0.05));
		//mq.add(new MsgBucketTime(10, 1.0));
		//mq.add(new MsgStop());
		
		mq.add(new MsgMotorValues());
		
		
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
