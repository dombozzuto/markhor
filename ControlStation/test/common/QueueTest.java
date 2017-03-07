package common;
import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

public class QueueTest {
	
	private MessageQueue mq;
	
	@Before
	public void setup()
	{
		mq = new MessageQueue();
	}

	@Test
	public void queueIsCreated()
	{
		assertNotNull(mq);
		assertEquals(0, mq.getSize());
		assertTrue(mq.isEmpty());
	}

}
