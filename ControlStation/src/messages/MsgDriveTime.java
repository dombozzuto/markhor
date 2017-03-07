package messages;

import common.AbsMessage;
import common.MessageType;

public class MsgDriveTime extends AbsMessage 
{

	public MsgDriveTime(int time, int speed)
	{
		setType(MessageType.MSG_DRIVE_TIME);
		setSize(2);
		setInfo("Driving for " + time + "ms at speed:" + speed + "\n");
	}
}
