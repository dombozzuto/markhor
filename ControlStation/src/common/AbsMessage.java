package common;

public abstract class AbsMessage implements Message
{
	private MessageType type;
	private int size;
	private String info;
	
	public AbsMessage() {}

	public MessageType getType() {return type;}
	public void setType(MessageType type) {this.type = type;}

	public int getSize() {return size;}
	public void setSize(int size) {this.size = size;}

	public String getInfo() {return info;}
	public void setInfo(String info) {this.info = info;}
	
	
	
}
