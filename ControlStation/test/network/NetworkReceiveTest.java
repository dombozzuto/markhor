package network;

public class NetworkReceiveTest {
	
	public static void main(String [] args)
	{
		final int port = 11000;
		NetworkServer server = new NetworkServer(port);
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
