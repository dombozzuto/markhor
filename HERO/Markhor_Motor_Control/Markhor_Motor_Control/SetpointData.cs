using System;
using System.Text;
using Microsoft.SPOT;

namespace Markhor_Motor_Control
{
    class SetpointData
    {
        private int deviceID;
        private int setpoint;
        private float setpoint_converted;
        private CTRE.TalonSrx.ControlMode mode;
        public SetpointData(int deviceID, int mode, int setpoint)
        {
            this.deviceID = deviceID;
            this.mode = (CTRE.TalonSrx.ControlMode)mode;
            this.setpoint = setpoint;
            setpoint_converted = convertSetpoint();
        }

        public int getDeviceID() { return deviceID; }
        public int getRawSetpoint() { return setpoint; }
        public float getConvertedSetpoint() { return setpoint_converted; }
        public CTRE.TalonSrx.ControlMode getMode() { return mode; }


        private float convertSetpointToVbus()
        {
            return (float)(setpoint / 1000.0);
        }

        private float convertSetpointToCurrent()
        {
            return (float)(setpoint / 1000.0);
        }

        private float convertSetpoint()
        {
            switch(mode)
            {
                case CTRE.TalonSrx.ControlMode.kPercentVbus:
                    return convertSetpointToVbus();
                case CTRE.TalonSrx.ControlMode.kCurrent:
                    return convertSetpointToCurrent();
                default:
                    return (float)0.0;
            }
        }


    }
}
