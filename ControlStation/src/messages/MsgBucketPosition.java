package messages;

import common.AbsMessage;
import common.MessageType;

public class MsgBucketPosition extends AbsMessage 
{
	public MsgBucketPosition(double position, double speed)
	{
		super();
		setType(MessageType.MSG_BUCKET_POSITION);
		setSize(2);
		setInfo("Moving winch to position" + position + "m at speed:" + speed + "\n");
		
		setDataByIndex(0, position);
		setDataByIndex(1, speed);
		
	}
}
