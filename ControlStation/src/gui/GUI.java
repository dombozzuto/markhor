package gui;

import javax.swing.JFrame;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.GridBagLayout;
import javax.swing.JPanel;
import java.awt.Point;
import javax.swing.SpringLayout;
import javax.swing.JTabbedPane;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.JButton;
import javax.swing.JList;
import java.awt.Color;
import javax.swing.JLabel;
import javax.swing.JComboBox;
import javax.swing.JRadioButton;
import javax.swing.JTextField;
import java.awt.Font;
import java.awt.List;
import javax.swing.SwingConstants;

import common.Message;
import common.MessageFactory;
import common.MessageQueue;
import common.MessageType;
import messages.*;

import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class GUI extends JFrame{
	
	private JFrame frame;
	
	private JTextField txtSupposedToBe;
	private JTextField textField_6;
	private JTextField tbox_data0;
	private JTextField tbox_data1;
	private JTextField tbox_data2;
	private JTextField tbox_data3;
	private JTextField tbox_data4;
	private JTextField tbox_data5;
	private JTextField tbox_data6;
	private JTextField tbox_data7;
	
	private MessageQueue messageQueue;
	private MessageType selectedMessageType = MessageType.MSG_STOP;
	private Message selectedMessage = new MsgStop();
	private JLabel[] messageLabels = new JLabel[8];
	
	public static void main(String[] args) 
	{
		MessageQueue messageQueue = new MessageQueue();
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					GUI window = new GUI(messageQueue);
					window.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	
	private void initialize(MessageQueue messageQueue)
	{
		this.messageQueue = messageQueue;
		
		frame = new JFrame();
		frame.setBounds(0, 0, 1600, 900);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		 
		setTitle("Markhor.exe");
		setSize(new Dimension(1600, 900));
		setResizable(false);
		
		JTabbedPane tabbedPane = new JTabbedPane(JTabbedPane.TOP);
		tabbedPane.setMaximumSize(new Dimension(785, 32767));
		
		JPanel panel = new JPanel();
		panel.setBackground(Color.LIGHT_GRAY);
		
		
		
		JPanel panel_1 = new JPanel();
		
		
		
		JLabel lblStatus = new JLabel("Status:");
		
		JLabel lblResolution = new JLabel("Resolution");
		
		JComboBox<String> comboBox = new JComboBox<String>();
		
		JRadioButton rdbtnEnabled = new JRadioButton("Enabled");
		GroupLayout groupLayout = new GroupLayout(getContentPane());
		groupLayout.setHorizontalGroup(
			groupLayout.createParallelGroup(Alignment.TRAILING)
				.addGroup(groupLayout.createSequentialGroup()
					.addContainerGap()
					.addGroup(groupLayout.createParallelGroup(Alignment.LEADING)
						.addComponent(panel_1, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
						.addGroup(groupLayout.createSequentialGroup()
							.addComponent(tabbedPane, GroupLayout.PREFERRED_SIZE, 787, GroupLayout.PREFERRED_SIZE)
							.addPreferredGap(ComponentPlacement.UNRELATED)
							.addGroup(groupLayout.createParallelGroup(Alignment.LEADING)
								.addGroup(groupLayout.createSequentialGroup()
									.addComponent(lblResolution)
									.addPreferredGap(ComponentPlacement.RELATED)
									.addComponent(comboBox, GroupLayout.PREFERRED_SIZE, 117, GroupLayout.PREFERRED_SIZE)
									.addPreferredGap(ComponentPlacement.UNRELATED)
									.addComponent(rdbtnEnabled)
									.addPreferredGap(ComponentPlacement.RELATED, 501, Short.MAX_VALUE))
								.addComponent(panel, GroupLayout.DEFAULT_SIZE, 777, Short.MAX_VALUE)))
						.addComponent(lblStatus))
					.addContainerGap())
		);
		groupLayout.setVerticalGroup(
			groupLayout.createParallelGroup(Alignment.LEADING)
				.addGroup(groupLayout.createSequentialGroup()
					.addContainerGap()
					.addGroup(groupLayout.createParallelGroup(Alignment.LEADING, false)
						.addGroup(Alignment.TRAILING, groupLayout.createSequentialGroup()
							.addComponent(panel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
							.addPreferredGap(ComponentPlacement.UNRELATED)
							.addGroup(groupLayout.createParallelGroup(Alignment.BASELINE)
								.addComponent(lblResolution)
								.addComponent(comboBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
								.addComponent(rdbtnEnabled)))
						.addComponent(tabbedPane, GroupLayout.PREFERRED_SIZE, 594, GroupLayout.PREFERRED_SIZE))
					.addPreferredGap(ComponentPlacement.RELATED, 15, Short.MAX_VALUE)
					.addComponent(lblStatus)
					.addPreferredGap(ComponentPlacement.RELATED)
					.addComponent(panel_1, GroupLayout.PREFERRED_SIZE, 220, GroupLayout.PREFERRED_SIZE)
					.addContainerGap())
		);
		
		JList<String> list_1 = new JList<String>();
		GroupLayout gl_panel_1 = new GroupLayout(panel_1);
		gl_panel_1.setHorizontalGroup(
			gl_panel_1.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_panel_1.createSequentialGroup()
					.addContainerGap()
					.addComponent(list_1, GroupLayout.DEFAULT_SIZE, 1362, Short.MAX_VALUE)
					.addGap(37))
		);
		gl_panel_1.setVerticalGroup(
			gl_panel_1.createParallelGroup(Alignment.TRAILING)
				.addGroup(gl_panel_1.createSequentialGroup()
					.addContainerGap()
					.addComponent(list_1, GroupLayout.DEFAULT_SIZE, 220, Short.MAX_VALUE))
		);
		panel_1.setLayout(gl_panel_1);
		
		JPanel panel_2 = new JPanel();
		tabbedPane.addTab("Main", null, panel_2, null);
		
		JButton btnRemoveSelected = new JButton("Remove");
		btnRemoveSelected.setBackground(new Color(0, 0, 128));
		btnRemoveSelected.setForeground(new Color(255, 255, 255));
		btnRemoveSelected.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnRemoveSelected.setPreferredSize(new Dimension(100, 100));
		
		JButton btnClearAll = new JButton("Clear All");
		btnClearAll.setBackground(new Color(0, 0, 128));
		btnClearAll.setForeground(new Color(255, 255, 255));
		btnClearAll.setFont(new Font("Tahoma", Font.PLAIN, 20));
		
		JButton btnStop = new JButton("STOP");
		btnStop.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnStop.setForeground(new Color(255, 255, 255));
		btnStop.setBackground(new Color(255, 0, 0));
		
		JList<String> list = new JList<String>();
		
		JButton btnStartQueue = new JButton("START");
		btnStartQueue.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnStartQueue.setBackground(new Color(0, 128, 0));
		btnStartQueue.setForeground(new Color(255, 255, 255));
		GroupLayout gl_panel_2 = new GroupLayout(panel_2);
		gl_panel_2.setHorizontalGroup(
			gl_panel_2.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_panel_2.createSequentialGroup()
					.addContainerGap()
					.addComponent(list, GroupLayout.PREFERRED_SIZE, 616, GroupLayout.PREFERRED_SIZE)
					.addGap(18)
					.addGroup(gl_panel_2.createParallelGroup(Alignment.LEADING)
						.addComponent(btnStop, Alignment.TRAILING, GroupLayout.DEFAULT_SIZE, 128, Short.MAX_VALUE)
						.addComponent(btnStartQueue, GroupLayout.DEFAULT_SIZE, 128, Short.MAX_VALUE)
						.addComponent(btnClearAll, GroupLayout.DEFAULT_SIZE, 128, Short.MAX_VALUE)
						.addComponent(btnRemoveSelected, GroupLayout.PREFERRED_SIZE, 129, GroupLayout.PREFERRED_SIZE))
					.addContainerGap())
		);
		gl_panel_2.setVerticalGroup(
			gl_panel_2.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_panel_2.createSequentialGroup()
					.addContainerGap()
					.addGroup(gl_panel_2.createParallelGroup(Alignment.LEADING)
						.addComponent(list, GroupLayout.DEFAULT_SIZE, 544, Short.MAX_VALUE)
						.addGroup(gl_panel_2.createSequentialGroup()
							.addComponent(btnRemoveSelected, GroupLayout.PREFERRED_SIZE, 125, GroupLayout.PREFERRED_SIZE)
							.addPreferredGap(ComponentPlacement.RELATED)
							.addComponent(btnClearAll, GroupLayout.PREFERRED_SIZE, 87, GroupLayout.PREFERRED_SIZE)
							.addPreferredGap(ComponentPlacement.RELATED)
							.addComponent(btnStop, GroupLayout.PREFERRED_SIZE, 114, GroupLayout.PREFERRED_SIZE)
							.addPreferredGap(ComponentPlacement.RELATED)
							.addComponent(btnStartQueue, GroupLayout.DEFAULT_SIZE, 200, Short.MAX_VALUE)))
					.addContainerGap())
		);
		panel_2.setLayout(gl_panel_2);
		
		JPanel panel_3 = new JPanel();
		tabbedPane.addTab("Commands", null, panel_3, null);
		panel_3.setLayout(null);
		
		JPanel panel_5 = new JPanel();
		panel_5.setBounds(10, 11, 395, 515);
		panel_5.setLayout(null);
		
		JLabel lblCommandType = new JLabel("Command Type");
		lblCommandType.setBounds(10, 8, 140, 25);
		panel_5.add(lblCommandType);
		lblCommandType.setFont(new Font("Tahoma", Font.PLAIN, 20));
		
		JLabel lbl_data0 = new JLabel("Data 0");
		lbl_data0.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data0.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data0.setBounds(10, 58, 168, 31);
		panel_5.add(lbl_data0);
		
		JLabel lbl_data1 = new JLabel("Data 1");
		lbl_data1.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data1.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data1.setBounds(10, 100, 168, 31);
		panel_5.add(lbl_data1);
		
		JLabel lbl_data2 = new JLabel("Data 2");
		lbl_data2.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data2.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data2.setBounds(10, 142, 168, 31);
		panel_5.add(lbl_data2);
		
		JLabel lbl_data3 = new JLabel("Data 3");
		lbl_data3.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data3.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data3.setBounds(10, 184, 168, 31);
		panel_5.add(lbl_data3);
		
		JLabel lbl_data4 = new JLabel("Data 4");
		lbl_data4.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data4.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data4.setBounds(10, 226, 168, 31);
		panel_5.add(lbl_data4);
		
		JLabel lbl_data5 = new JLabel("Data 5");
		lbl_data5.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data5.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data5.setBounds(10, 268, 168, 31);
		panel_5.add(lbl_data5);
		
		JLabel lbl_data6 = new JLabel("Data 6");
		lbl_data6.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data6.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data6.setBounds(10, 310, 168, 31);
		panel_5.add(lbl_data6);
		
		JLabel lbl_data7 = new JLabel("Data 7");
		lbl_data7.setHorizontalAlignment(SwingConstants.TRAILING);
		lbl_data7.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lbl_data7.setBounds(10, 352, 168, 31);
		panel_5.add(lbl_data7);
		
		messageLabels[0] = lbl_data0;
		messageLabels[1] = lbl_data1;
		messageLabels[2] = lbl_data2;
		messageLabels[3] = lbl_data3;
		messageLabels[4] = lbl_data4;
		messageLabels[5] = lbl_data5;
		messageLabels[6] = lbl_data6;
		messageLabels[7] = lbl_data7;
		
		JComboBox<String> cbox_cmdType = new JComboBox<String>();
		cbox_cmdType.addItemListener(new ItemListener() {
			public void itemStateChanged(ItemEvent arg0) 
			{
				selectedMessageType = MessageType.values()[cbox_cmdType.getSelectedIndex()];
				selectedMessage = MessageFactory.makeMessage(selectedMessageType);
				updateMessageLabels();
				System.out.println("Selected a Message of Type: " + selectedMessageType.toString());
			}
		});
		cbox_cmdType.setBounds(160, 5, 225, 31);
		setCommandComboBoxStrings(cbox_cmdType);
		
		panel_5.add(cbox_cmdType);
		cbox_cmdType.setFont(new Font("Tahoma", Font.PLAIN, 20));
		
		panel_3.add(panel_5);
		
		
		
		tbox_data0 = new JTextField();
		tbox_data0.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data0.setColumns(10);
		tbox_data0.setBounds(188, 58, 197, 31);
		panel_5.add(tbox_data0);
		
		tbox_data1 = new JTextField();
		tbox_data1.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data1.setColumns(10);
		tbox_data1.setBounds(188, 100, 197, 31);
		panel_5.add(tbox_data1);
		
		tbox_data2 = new JTextField();
		tbox_data2.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data2.setColumns(10);
		tbox_data2.setBounds(188, 142, 197, 31);
		panel_5.add(tbox_data2);
		
		tbox_data3 = new JTextField();
		tbox_data3.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data3.setColumns(10);
		tbox_data3.setBounds(188, 184, 197, 31);
		panel_5.add(tbox_data3);

		tbox_data4 = new JTextField();
		tbox_data4.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data4.setColumns(10);
		tbox_data4.setBounds(188, 226, 197, 31);
		panel_5.add(tbox_data4);
		
		tbox_data5 = new JTextField();
		tbox_data5.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data5.setColumns(10);
		tbox_data5.setBounds(188, 268, 197, 31);
		panel_5.add(tbox_data5);
		
		tbox_data6 = new JTextField();
		tbox_data6.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data6.setColumns(10);
		tbox_data6.setBounds(188, 310, 197, 31);
		panel_5.add(tbox_data6);
		
		tbox_data7 = new JTextField();
		tbox_data7.setFont(new Font("Tahoma", Font.PLAIN, 20));
		tbox_data7.setColumns(10);
		tbox_data7.setBounds(188, 352, 197, 31);
		panel_5.add(tbox_data7);
		
		JButton btnAddToEnd = new JButton("Add to End");
		btnAddToEnd.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
			}
		});
		btnAddToEnd.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnAddToEnd.setBounds(10, 394, 375, 41);
		panel_5.add(btnAddToEnd);
		
		JButton btnAddAtPosition = new JButton("Add at Position");
		btnAddAtPosition.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnAddAtPosition.setBounds(10, 446, 247, 58);
		panel_5.add(btnAddAtPosition);
		
		textField_6 = new JTextField();
		textField_6.setFont(new Font("Tahoma", Font.PLAIN, 20));
		textField_6.setBounds(267, 446, 118, 58);
		panel_5.add(textField_6);
		textField_6.setColumns(10);
		
		JPanel panel_4 = new JPanel();
		tabbedPane.addTab("Misc", null, panel_4, null);
		
		txtSupposedToBe = new JTextField();
		txtSupposedToBe.setText("Supposed to be pictures of pizza");
		txtSupposedToBe.setColumns(10);
		GroupLayout gl_panel_4 = new GroupLayout(panel_4);
		gl_panel_4.setHorizontalGroup(
			gl_panel_4.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_panel_4.createSequentialGroup()
					.addContainerGap()
					.addComponent(txtSupposedToBe, GroupLayout.PREFERRED_SIZE, 617, GroupLayout.PREFERRED_SIZE)
					.addContainerGap(155, Short.MAX_VALUE))
		);
		gl_panel_4.setVerticalGroup(
			gl_panel_4.createParallelGroup(Alignment.LEADING)
				.addGroup(gl_panel_4.createSequentialGroup()
					.addContainerGap()
					.addComponent(txtSupposedToBe, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
					.addContainerGap(535, Short.MAX_VALUE))
		);
		panel_4.setLayout(gl_panel_4);
		
		getContentPane().setLayout(groupLayout);
		
		
	}
	
	private void updateMessageQueueList()
	{
		
	}
	
	private void setCommandComboBoxStrings(JComboBox<String> cbox)
	{
		cbox.addItem("STOP");
		cbox.addItem("Drive Time");
		cbox.addItem("Drive Distance");
		cbox.addItem("Rotate Time");
		cbox.addItem("Scoop Time");
		cbox.addItem("Scoop Distance");
		cbox.addItem("Depth Time");
		cbox.addItem("Depth Distance");
		cbox.addItem("Bucket Time");
		cbox.addItem("Bucket Distance");
		cbox.addItem("Bucket Position");
		cbox.addItem("Stop Time");
		cbox.addItem("Motor Values");
	}
	
	private void updateMessageLabels()
	{
		for(int i = 0; i < 8; i++)
		{
			System.out.println(selectedMessage.getDataTagByIndex(i));
			if(selectedMessage != null)
			{
				messageLabels[i].setText(selectedMessage.getDataTagByIndex(i));
			}
		}
	}

	public GUI(MessageQueue messageQueue) {
		initialize(messageQueue);
	}
}
