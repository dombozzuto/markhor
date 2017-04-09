package network;

import java.io.*;
import java.net.*;

import common.Gamepad;
import common.MessageQueue;
import gui.RobotData;

public class NetworkServer extends Thread
{
	private ServerSocket serverSocket;
	private MessageQueue queue;
	private RobotData robotData;
	private int port;
	private boolean running = false;
	private Gamepad g = new Gamepad();
	
	public NetworkServer(int port, MessageQueue queue, RobotData robotData)
	{
		this.port = port;
		this.queue = queue;
		this.robotData = robotData;
	}
	
	public void startServer()
	{
		try
		{
			if(serverSocket == null)
			{
				serverSocket = new ServerSocket(port);
			}
			this.start();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}
	
	public void stopServer() throws IOException
	{
		running = false;
		serverSocket.close();
		this.interrupt();
		serverSocket.close();
		
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
				RequestHandler requestHandler = new RequestHandler(socket, queue, robotData);
				requestHandler.start();
			}
			catch(IOException e)
			{
				e.printStackTrace();
			}
		}
	}

}
