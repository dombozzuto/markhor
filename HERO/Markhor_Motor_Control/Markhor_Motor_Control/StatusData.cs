using System;

namespace Markhor_Motor_Control
{
    class StatusData
    {   
        private int talonDeviceID;          //fixed device id
        private int talonCurrent;           //current in mA
        private int talonTemperature;       //temp in milli-degC
        private int talonVoltage;           //voltage in mV
        private int talonSpeed;             //encoder ticks/100ms
        private int talonSetpoint;          //setpoint based on control mode

        private CTRE.TalonSrx.ControlMode controlMode;    //talon control mode

        private int talonForwardLimitReached;
        private int talonReverseLimitReached;
        

        private CTRE.TalonSrx talon;

        public StatusData(int talonDeviceID, CTRE.TalonSrx talon)
        {
            this.talonDeviceID = talonDeviceID;
            this.talon = talon;
        }

        public void updateStatusData()
        {
            talonCurrent = (int)(talon.GetOutputCurrent() * 1000);
            talonTemperature = (int)(talon.GetTemperature() * 1000);
            talonVoltage = (int)(talon.GetOutputVoltage() * 1000);
            talonSpeed = (int)(talon.GetSpeed());
            talonSetpoint = (int)(talon.GetSetpoint() * 1000);
            talonForwardLimitReached = talon.IsFwdLimitSwitchClosed() ? 1 : 0;
            talonReverseLimitReached = talon.IsRevLimitSwitchClosed() ? 1 : 0;
            controlMode = talon.GetControlMode();
        }

        public String getOutboundMessage()
        {
            String outboundMessage = "<";

            outboundMessage += talonDeviceID.ToString() + ":";
            outboundMessage += talonCurrent.ToString() + ":";
            outboundMessage += talonTemperature.ToString() + ":";
            outboundMessage += talonVoltage.ToString() + ":";
            outboundMessage += talonSpeed.ToString() + ":";
            outboundMessage += talonSetpoint.ToString() + ":";

            outboundMessage += controlMode.ToString() + ":";

            outboundMessage += talonForwardLimitReached.ToString() + ":";
            outboundMessage += talonReverseLimitReached.ToString();

            outboundMessage += ">";
            return outboundMessage;
        }

        public String getOutboundMessage2()
        {
            return "<--->";
        }
    }
}
