package network;

import java.io.*;
import java.net.*;

import common.MessageQueue;

public class NetworkServer extends Thread
{
	private ServerSocket serverSocket;
	private MessageQueue queue;
	private int port;
	private boolean running = false;
	
	public NetworkServer(int port, MessageQueue queue)
	{
		this.port = port;
		this.queue = queue;
	}
	
	public void startServer()
	{
		try
		{
			serverSocket = new ServerSocket(port);
			this.start();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}
	
	public void stopServer()
	{
		running = false;
		this.interrupt();
	}
	
	@Override
	public void run()
	{
		running = true;
		while(running)
		{
			try
			{
				Socket socket = serverSocket.accept();
				RequestHandler requestHandler = new RequestHandler(socket, queue);
				requestHandler.start();
			}
			catch(IOException e)
			{
				e.printStackTrace();
			}
		}
	}

}
