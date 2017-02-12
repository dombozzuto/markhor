using System;
using Microsoft.SPOT;

namespace Markhor_Motor_Control
{
    class ControlData
    {
        private int deviceID;
        private int deviceMode;
        private float setpoint;

        public ControlData(int deviceID)
        {
            this.deviceID = deviceID;
            this.deviceMode = 0;
            this.setpoint = 0.0F;
        }

    }
}
