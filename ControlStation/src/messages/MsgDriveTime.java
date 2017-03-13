package messages;

import common.AbsMessage;
import common.MessageType;

public class MsgDriveTime extends AbsMessage 
{

	public MsgDriveTime(double time, double speed)
	{
		super();
		setType(MessageType.MSG_DRIVE_TIME);
		setSize(2);
		setInfo("Driving for " + time + "ms at speed:" + speed + "\n");
		
		setDataByIndex(0, time);
		setDataByIndex(1, speed);
		
	}
}
