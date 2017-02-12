using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication1
{
    class ControlData
    {
        private int deviceID;
        private int setpoint;
        private Double setpoint_converted;
        private char mode;

        private const int RAW_MIN = 0;
        private const int RAW_MAX = 10000;
        private const int RAW_MID = (RAW_MAX - RAW_MIN) / 2;
        private const Double SCALED_MIN = -1.0;
        private const Double SCALED_MAX = 1.0;

        public ControlData(int deviceID, char mode, int setpoint)
        {
            this.deviceID = deviceID;
            this.mode = mode;
            this.setpoint = setpoint;
            setpoint_converted = convertRawToSetpoint(setpoint);
        }

        private Double convertRawToSetpoint(int setpoint)
        {
            Double scaledSetpoint;
            setpoint -= RAW_MID;
            scaledSetpoint = ((Double)setpoint / (Double)RAW_MID);
            return scaledSetpoint;
        }
    }
}
