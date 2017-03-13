package messages;

import common.AbsMessage;
import common.MessageType;

public class MsgScoopTime extends AbsMessage
{
	public MsgScoopTime(double time, double speed)
	{
		super();
		setType(MessageType.MSG_SCOOP_TIME);
		setSize(2);
		setInfo("Running scoops for " + time + "s at speed:" + speed + "\n");
		
		setDataByIndex(0, time);
		setDataByIndex(1, speed);	
	}
}
