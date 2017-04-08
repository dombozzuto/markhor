package data;

import common.MotorMode;

/*
 * 	msg_deviceID = int(match[0])
	msg_current = float(match[1])
	msg_temperature = float(match[2])
	msg_voltageOutput = float(match[3])
	msg_speed = float(match[4])
	msg_position = float(match[5])
	msg_setpoint = float(match[6])
	msg_controlMode = int(match[7])
	msg_forward_limit = bool(int(match[8]))
	msg_reverse_limit = bool(int(match[9]))
 * 
 */

public class Motor 
{
	private Integer deviceID = -1;
	private Double current = Double.NaN;
	private Double temperature = Double.NaN;
	private Double voltage = Double.NaN;
	private Double speed = Double.NaN;
	private Double position = Double.NaN;
	private Double setpoint = Double.NaN;
	private MotorMode mode = MotorMode.K_PERCENT_VBUS;
	private Boolean forward_limit = false;
	private Boolean reverse_limit = false;
	
	public Motor(){}

	public Integer getDeviceID() {return deviceID;}
	public Double getCurrent() {return current;}
	public Double getTemperature() {return temperature;}
	public Double getVoltage() {return voltage;}
	public Double getSpeed() {return speed;}
	public Double getPosition() {return position;}
	public Double getSetpoint() {return setpoint;}
	public MotorMode getMode() {return mode;}
	public Boolean getForwardLimit() {return forward_limit;}
	public Boolean getReverseLimit() {return reverse_limit;}
	
	public void setDeviceID(Integer deviceID) {this.deviceID = deviceID;}
	public void setCurrent(Double current) {this.current = current;}
	public void setTemperature(Double temperature) {this.temperature = temperature;}
	public void setVoltage(Double voltage) {this.voltage = voltage;}
	public void setSpeed(Double speed) {this.speed = speed;}
	public void setPosition(Double position) {this.position = position;}
	public void setSetpoint(Double setpoint) {this.setpoint = setpoint;}
	public void setMode(MotorMode mode) {this.mode = mode;}
	public void setForwardLimit(Boolean forward_limit) {this.forward_limit = forward_limit;}
	public void setReverseLimit(Boolean reverse_limit) {this.reverse_limit = reverse_limit;}	
}
