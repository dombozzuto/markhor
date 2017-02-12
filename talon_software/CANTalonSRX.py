from TrajectoryBuffer import TrajectoryBuffer

# A port of the TalonSRX SDK LowLevel_TalonSRX to Python from C#

class LowLevel_TalonSRX:

    STATUS_1 = 0x02041400
    STATUS_2 = 0x02041440
    STATUS_3 = 0x02041480
    STATUS_4 = 0x020414C0
    STATUS_5 = 0x02041500
    STATUS_6 = 0x02041540
    STATUS_7 = 0x02041580
    STATUS_8 = 0x020415C0
    STATUS_9 = 0x02041600
    STATUS_10= 0x02041640

    CONTROL_1 = 0x02040000
    CONTROL_2 = 0x02040040
    CONTROL_3 = 0x02040080
    CONTROL_5 = 0x02040100
    CONTROL_6 = 0x02040140

    PARAM_REQUEST = 0x02041800
    PARAM_RESPONSE = 0x02041840
    PARAM_SET = 0x02041880

    kParamArbIdValue = PARAM_RESPONSE
    kParamArbIdMask = 0xFFFFFFFF

    FLOAT_TO_FXP_10_22 = float(0x400000)
    FXP_TO_FLOAT_10_22 = 0.0000002384185791015625

    FLOAT_TO_FXP_0_8 = float(0x100)
    FXP_TO_FLOAT_0_8 = 0.00390625

    # status frame rate types
    kStatusFrame_General = 0
    kStatusFrame_Feedback = 1
    kStatusFrame_Encoder = 2
    kStatusFrame_AnalogTempVbat = 3
    kStatusFrame_PulseWidthMeas = 4
    kStatusFrame_MotionProfile = 5
    kStatusFrame_MotionMagic = 6
    
    # Motion Profile status bits 
    kMotionProfileFlag_ActTraj_IsValid = 0x1
    kMotionProfileFlag_HasUnderrun = 0x2
    kMotionProfileFlag_IsUnderrun = 0x4
    kMotionProfileFlag_ActTraj_IsLast = 0x8
    kMotionProfileFlag_ActTraj_VelOnly = 0x10
    
    # Motion Profile Set Output 
    # Motor output is neutral, Motion Profile Executer is not running.
    kMotionProf_Disabled = 0
    
    # Motor output is updated from Motion Profile Executer, MPE will
    # process the buffered points.
    kMotionProf_Enable = 1
    
    # Motor output is updated from Motion Profile Executer, MPE will
    # stay processing current trajectory point.
    kMotionProf_Hold = 2

    kDefaultControl6PeriodMs = 10

    _cache = None
    _len = None
    _can_h = 0
    _can_stat = 0

    #--------------------- Buffering Motion Profile ---------------------------#

    """
     * To keep buffers from getting out of control, place a cap on the top level
     * buffer.  Calling application
     * can stream addition points as they are fed to Talon.
     * Approx memory footprint is this capacity X 8 bytes.
    """

    kMotionProfileTopBufferCapacity = 512
    _motProfTopBuffer = TrajectoryBuffer(kMotionProfileTopBufferCapacity)
    
    _motProfFlowControl = -1

    ## TODO: FIGURE OUT THIS
    # _mutMotProf = new Object()

    _control6PeriodMs = kDefaultControl6PeriodMs

    _sigs = {}

    def __init__(self, deviceID, externalEnable=False): # : base(deviceID)
        if(False == externalEnable):
            CTRE.Native.CAN.Send(CONTROL_1 | self._deviceNumber, 0x00, 2, 50)
            CTRE.Native.CAN.Send(CONTROL_5 | self._deviceNumber, 0x00, 8, 10)
            self.SetOverrideLimitSwitchEn(1)

    def OpenSessionIfNeedBe(self):
        self._can_stat = 0;
        if(self._can_h == 0):
            # bit30 - bit8 must match $000002XX.  Top bit is not masked to get remote frames #
            arbID = self.kParamArbIdValue | self.GetDeviceNumber()
            self._can_stat = CTRE.Native.CAN.OpenStream(self._can_h, self.kParamArbIdMask, arbID)
            if(self._can_stat == 0):
                # success
                pass
            else:
                # something went wrong, try again later
                _can_h = 0
                
    #TODO: Resolve pass by reference issues
    def ProcessStreamMessages(self):
        if(0 == self._can_h):
            self.OpenSessionIfNeedBe()

        # process receive messages #
        messagesRead = 0
        arbId = 0
        data = 0
        length = 0
        msgsRead = 0

        # read out latest bunch of messages #
        self._can_stat = 0
        if(self._can_h != 0):
            messagesRead = CTRE.Native.CAN.GetStreamSize(self._can_h)

        for i in range(messagesRead):
            CTRE.Native.CAN.ReadStream(self._can_h, ref arbId, ref data, ref length, ref msgsRead)
            if(arbId == (self.PARAM_RESPONSE | self.GetDeviceNumber())):
                paramEnum = (data & 0xFF)
                data = (data >> 8)
                self._sigs[paramEnum] = data


    def Set(self, value, controlMode):
        if(value > 1.0):
            value = 1.0
        elif(value < -1.0):
            value = -1.0
        # must be within [-1023,1023] #
        SetDemand24(int(1023*value), controlMode)

    ##---------------------setters and getters that use the param request/response-------------##
    """
     * Send a one shot frame to set an arbitrary signal.
     * Most signals are in the control frame so avoid using this API unless you have
     * to.
     * Use this api for...
     * -A motor controller profile signal eProfileParam_XXXs.  These are backed up
     * in flash.  If you are gain-scheduling then call this periodically.
     * -Default brake and limit switch signals... eOnBoot_XXXs.  Avoid doing this,
     * use the override signals in the control frame.
     * Talon will automatically send a PARAM_RESPONSE after the set, so
     * GetParamResponse will catch the latest value after a couple ms.
    """

    def SetParamRaw(self, paramEnum, rawBits, timeoutMs=0):
        # caller is using param API.  Open session if it hasn'T been done. #
        if(0 == self._can_h):
            self.OpenSessionIfNeedBe()
        # wait for response frame #
        if(timeoutMs != 0):
            # remove stale entry if caller wants to wait for response. #
            del self._sigs[paramEnum]
        # fram set request and send it #
        frame = rawBits & 0xFFFFFFFF
        frame = (frame << 8)
        frame |= (paramEnum & 0x000000FF)

        arbId = PARAM_SET | self.GetDeviceNumber()
        status = CTRE.Native.CAN.Send(arbId, frame, 5, 0)
        # wait for response frame #
        if(timeoutMs > 0):
            readBits = None
            # loop until timeout or receive if caller wants to check
            while(timeoutMs > 0):
                # wait a bit
                time.sleep(0.001)
                if(0 == self.GetParamResponseRaw(paramEnum, out readBits)):
                    break
                timeoutMs -= 1
            # if we get here then we timed out #
            if(timeoutMs == 0):
                status = Codes.CTR_SigNotUpdated
        return status

    """
     * Checks cached CAN frames and updating solicited signals.
    """    
    def GetParamResponseRaw(self, paramEnum, out rawBits):
        retval = 0
        # process received param events. We don't expect many since this API is not* used often. #
        self.ProcessStreamMessages()
        if((paramEnum in self._sigs) == False):
            retval = Codes.CTR_SigNotUpdated
            rawBits = 0
        else:
            value = _sigs[paramEnum]
            temp = value
            rawBits = temp
        return retval

    """
     * Asks TALON to immedietely respond with signal value.  This API is only used
     * for signals that are not sent periodically.
     * This can be useful for reading params that rarely change like Limit Switch
     * settings and PIDF values.
     * @param param to request.
    """
    def RequestParam(self, paramEnum):
        # process received param events. We don't expect many since this API is not used often. #
        self.ProcessStreamMessages()
        status = CTRE.Native.CAN.Send(self.PARAM_REQUEST | GetDeviceNumber(), paramEnum, 1, 0)
        return status


    def SetParam(self, paramEnum, value, timeoutMs=0):
        rawbits = 0
        if(paramEnum == ParamEnum.eProfileParamSlot0_P or
           paramEnum == ParamEnum.eProfileParamSlot0_I or
           paramEnum == ParamEnum.eProfileParamSlot0_D or
           paramEnum == ParamEnum.eProfileParamSlot1_P or
           paramEnum == ParamEnum.eProfileParamSlot1_I or
           paramEnum == ParamEnum.eProfileParamSlot1_D):
            if(value > 1023):
                value = 1023 #bounds check doubles that are outside u10.22 #
            elif(value < 0):
                value = 0
            #TODO this probably wont work because its bit manipulation and needs fixing
            urawbits = int(value * self.FLOAT_TO_FXP_10_22)
            rawbits = int(urawbits)

        # signed 10.22 fixed pt value #
        elif(paramEnum == ParamEnum.eProfileParamSlot1_F || paramEnum == ParamEnum.eProfileParamSlot0_F):
            if(value > 512): # bounds check doubles that are outside s10.22 #
                value = 512
            elif(value < -512):
                value = -512
            rawbits = int(value * self.FLOAT_TO_FXP_10_22)

        """ unsigned 0.8 fixed pt value volts per ms 
         * within [0,1) volts per ms.
         * Slowest ramp is 1/256 VperMilliSec or 3.072 seconds from 0-to-12V.
         * Fastest ramp is 255/256 VperMilliSec or 12.1ms from 0-to-12V.
        """
        elif(paramEnum == ParamEnum.eProfileParamVcompRate):
            if(value <= 0):
                # negative or zero (disable), send raw value of zero #
                rawbits = 0
            else:
                # nonzero ramping #
                rawbits = int(value * self.FLOAT_TO_FXP_0_8)
                # since whole part is cleared, cap to just under whole unit #
                if(rawbits > (self.FLOAT_TO_FXP_0_8 - 1)):
                    rawbits = int(self.FLOAT_TO_FXP_0_8 - 1)
                # since ramping is nonzero, cap to smallest ramp rate possible #
                if(rawbits == 0):
                    rawbits = 1

        else:
            rawbits = int(value)

        return self.SetParamRaw(paramEnum, rawbits, timeoutMs)

    def GetParamResponse(self, paramEnum, out value):
        rawbits = 0
        retval = self.GetParamResponseRaw(paramEnum, out rawbits)

        if(paramEnum == ParamEnum.eProfileParamSlot0_P or
           paramEnum == ParamEnum.eProfileParamSlot0_I or
           paramEnum == ParamEnum.eProfileParamSlot0_D or
           paramEnum == ParamEnum.eProfileParamSlot0_F or
           paramEnum == ParamEnum.eProfileParamSlot1_P or
           paramEnum == ParamEnum.eProfileParamSlot1_I or
           paramEnum == ParamEnum.eProfileParamSlot1_D or
           paramEnum == ParamEnum.eProfileParamSlot1_F or
           paramEnum == ParamEnum.eCurrent or
           paramEnum == ParamEnum.eTemp or
           paramEnum == ParamEnum.eBatteryV):
            value = float(rawbits) * self.FXP_TO_FLOAT_10_22

        elif(paramEnum ==ParamEnum.eProfileParamVcompRate):
            value = float(rawbits) * self.FXP_TO_FLOAT_0_8

        else:
            value = float(rawbits)

        return retval
                    
    def GetParamResponseInt32(self, paramEnum, out value):
        dvalue = 0.0
        retval = self.GetParamResponse(paramEnum, out dvalue)
        value = int(dvalue)
        return retval

    #----- getters and setters that use param request/response. These signals are backed up in flash and will survive a power cycle. ---------#
    #----- If your application requires changing these values consider using both slots and switch between slot0 <=> slot1. ------------------#
    #----- If your application requires changing these signals frequently then it makes sense to leverage this API. --------------------------#
    #----- Getters don't block, so it may require several calls to get the latest value. --------------------------#
    def SetPgain(self, slodIdx, gain, timeoutMs=0):
        if(slotIdx == 0):
            return self.SetParam(ParamEnum.eProfileParamSlot0_P, gain, timeoutMs)
        return self.SetParam(ParamEnum.eProfileParamSlot1_P, gain, timeoutMs)

    def SetIgain(self, slodIdx, gain, timeoutMs=0):
        if(slotIdx == 0):
            return self.SetParam(ParamEnum.eProfileParamSlot0_I, gain, timeoutMs)
        return self.SetParam(ParamEnum.eProfileParamSlot1_I, gain, timeoutMs)

    def SetDgain(self, slodIdx, gain, timeoutMs=0):
        if(slotIdx == 0):
            return self.SetParam(ParamEnum.eProfileParamSlot0_D, gain, timeoutMs)
        return self.SetParam(ParamEnum.eProfileParamSlot1_D, gain, timeoutMs)

    def SetFgain(self, slodIdx, gain, timeoutMs=0):
        if(slotIdx == 0):
            return self.SetParam(ParamEnum.eProfileParamSlot0_F, gain, timeoutMs)
        return self.SetParam(ParamEnum.eProfileParamSlot1_F, gain, timeoutMs)

    def SetIzone(self, slotIdx, zone, timeoutMs=0):
        if(slotIdx == 0):
            return self.SetParam(ParamEnum.eProfileParamSlot0_IZone, zone, timeoutMs)
        return self.SetParam(ParamEnum.eProfileParamSlot1_IZone, zone, timeoutMs)

    def SetCloseLoopRampRate(self, slotIdx, closeLoopRampRate, timeoutMs=0):
        if(slotIdx == 0):
            return self.SetParam(ParamEnum.eProfileParamSlot0_CloseLoopRampRate, closeLoopRampRate, timeoutMs)
        return self.SetParam(ParamEnum.eProfileParamSlot1_CloseLoopRampRate, closeLoopRampRate, timeoutMs)

    def SetVoltageCompensationRate(self, voltagePerMs, timeoutMs=0):
        return self.SetParam(ParamEnum.eProfileParamVcompRate, voltagePerMs, timeoutMs)


    def GetPgain(self, slotIdx, out gain):
        if(slotIdx == 0):
            return self.GetParamResponse(ParamEnum.eProfileParamSlot0_P, out gain)
        return self.GetParamResponse(ParamEnum.eProfileParamSlot1_P, out gain)

    def GetIgain(self, slotIdx, out gain):
        if(slotIdx == 0):
            return self.GetParamResponse(ParamEnum.eProfileParamSlot0_I, out gain)
        return self.GetParamResponse(ParamEnum.eProfileParamSlot1_I, out gain)
    
    def GetDgain(self, slotIdx, out gain):
        if(slotIdx == 0):
            return self.GetParamResponse(ParamEnum.eProfileParamSlot0_D, out gain)
        return self.GetParamResponse(ParamEnum.eProfileParamSlot1_D, out gain)
    
    def GetFgain(self, slotIdx, out gain):
        if(slotIdx == 0):
            return self.GetParamResponse(ParamEnum.eProfileParamSlot0_F, out gain)
        return self.GetParamResponse(ParamEnum.eProfileParamSlot1_F, out gain)


    def GetIzone(self, slotIdx, out zone):
        if(slotIdx == 0):
            return self.GetParamResponseInt32(ParamEnum.eProfileParamSlot0_IZone, out zone)
        return self.GetParamResponseInt32(ParamEnum.eProfileParamSlot1_IZone, out zone)

    def GetCloseLoopRampRate(self, slotIdx, out closeLoopRampRate):
        if(slotIdx == 0):
            return self.GetParamResponseInt32(ParamEnum.eProfileParamSlot0_CloseLoopRampRate, out closeLoopRampRate)
        return self.GetParamResponseInt32(ParamEnum.eProfileParamSlot1_CloseLoopRampRate, out closeLoopRampRate)

    def GetVoltageCompensationRate(self, out voltagePerMs):
        return self.GetParamResponse(ParamEnum.eProfileParamVcompRate, out voltagePerMs)

    def SetSensorPosition(self, pos, timeoutMs=0):
        return self.SetParam(ParamEnum.eSensorPosition, pos, timeoutMs)

    def SetForwardSoftLimit(self, forwardLimit, timeoutMs=0):
        return self.SetParam(ParamEnum.eProfileParamSoftLimitForThreshold, forwardLimit, timeoutMs)

    def SetReverseSoftLimit(self, reverseLimit, timeoutMs=0):
        return self.SetParam(ParamEnum.eProfileParamSoftLimitRevThreshold, reverseLimit, timeoutMs)

    def SetForwardSoftEnable(self, enable, timeoutMs=0):
        return self.SetParam(ParamEnum.eProfileParamSoftLimitForEnable, enable, timeoutMs)

    def SetReverseSoftEnable(self, enable, timeoutMs=0):
        return self.SetParam(ParamEnum.eProfileParamSoftLimitRevEnable, enable, timeoutMs)
    
    def GetForwardSoftLimit(self, out forwardLimit):
        return self.GetParamResponseInt32(ParamEnum.eProfileParamSoftLimitForThreshold, out forwardLimit)

    def GetReverseSoftLimit(self, out reverseLimit):
        return self.GetParamResponseInt32(ParamEnum.eProfileParamSoftLimitRevThreshold, out reverseLimit);

    def GetForwardSoftEnable(self, out enable):
        return self.GetParamResponseInt32(ParamEnum.eProfileParamSoftLimitForEnable, out enable);

    def GetReverseSoftEnable(self, out enable):
        return self.GetParamResponseInt32(ParamEnum.eProfileParamSoftLimitRevEnable, out enable);

    """
     * @param param [out] Rise to fall time period in microseconds.
    """
    def GetPulseWidthRiseToFallUs(self, out param):
        BIT12 = (1 << 12)
        temp = 0
        periodUs = 0
        # first grab our 12.12 position #
        retval1 = self.GetPulseWidthPosition(out temp)
        # mask off number of turns #
        temp = (temp & 0xFFF)
        # next grab the waveform period. This value will be zero if we stop getting pulses #
        retval2 = self.GetPulseWidthRiseToRise(out periodUs)
        # now we have 0.12 position that is scaled to the waveform period. #
        # Use fixed pt multiply to scale our 0.16 period into us. #
        param = (temp * periodUs) / BIT12
        # pass the worst error code to caller. Assume largest value is the most pressing error code. #
        if(retval1 > retval2):
            return retval1
        return retval2
    
    def IsPulseWidthSensorPresent(self, out param):
        periodUs = 0
        retval = self.GetPulseWidthRiseToRiseUs(out periodUs)
        if(periodUs != 0):
            param = 1
        else
            param = 0
        return retval

    """
     * Change the periodMs of a TALON's status frame.  See kStatusFrame_* enums for
     * what's available.
    """
    def SetStatusFrameRate(self, frameEnum, periodMs, timeoutMs=0):
        retval = Codes.CAN_OK
        paramEnum = 0
        # bounds check the period #
        if(periodMs < 1):
            periodMs = 1
        elif(periodMs > 255):
            periodMs = 255
        #TODO handle this bit transformation
        period = (0xFF & periodMs)
        #lookup the correct param enum based on what frame to rate-change #
        if(frameEnum == self.kStatusFrame_General):
            paramEnum = ParamEnum.eStatus1FrameRate
            
        elif(frameEnum == self.kStatusFrame_Feedback):
            paramEnum = ParamEnum.eStatus2FrameRate
            
        elif(frameEnum == self.kStatusFrame_Encoder):
            paramEnum = ParamEnum.eStatus3FrameRate
            
        elif(frameEnum == self.kStatusFrame_AnalogTempVbat):
            paramEnum = ParamEnum.eStatus4FrameRate
            
        elif(frameEnum == self.kStatusFrame_PulseWidthMeas):
            paramEnum = ParamEnum.eStatus8FrameRate                   

        elif(frameEnum == self.kStatusFrame_MotionProfile):
            paramEnum = ParamEnum.eStatus9FrameRate
    
        elif(frameEnum == self.kStatusFrame_MotionMagic):
            paramEnum = ParamEnum.eStatus10FrameRate

        else:
            # caller's request is not support, return an error code #
            retval = Codes.CAN_INVALID_PARAM
            
        # if lookup was succesful, send set-request out #
        if(retval == Codes.CAN_OK):
            # paramEnum is updated, sent it out #
            retval = self.SetParamRaw(paramEnum, period, timeoutMs)

        return int(retval)

    """
     * Clear all sticky faults in TALON.
    """
    def ClearStickyFaults(self):
        bit1 = 0x2
        return CTRE.Native.CAN.Send(self.CONTROL_3 | self.GetDeviceNumber(), bit1, 1, 0)

    """
     * @return the tx task that transmits Control6 (motion profile control).
     *         If it's not scheduled, then schedule it.  This is part of firing
     *         the MotionProf framing only when needed to save bandwidth.
    """
    def GetControl16(self):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_6 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            # control6 never started, arm it now #
            self._cache = 0
            CTRE.Native.CAN.Send(self.CONTROL_6 | self._deviceNumber, self._cache, 8, self._control6PeriodMs)
            # sync flow control #
            self._motProfFlowControl = 0
        return self._cache

    """
     * Calling application can opt to speed up the handshaking between the robot API
     * and the Talon to increase the download rate of the Talon's Motion Profile.
     * Ideally the period should be no more than half the period of a trajectory
     * point.
    """
    def ChangeMotionControlFramePeriod(self, periodMs):
        #TODO test this, involves semaphores
        #LOCK _mutMotProf
        """ if message is already registered, it will get updated.
         * Otherwise it will error if it hasn't been setup yet, but that's ok
         * because the _control6PeriodMs will be used later.
         * @see GetControl6
        """
        self._control6PeriodMs = periodMs
        # apply the change if the frame is transmitting #
        stat = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_6 | self._deviceNumber, ref self._cache)
        if(stat == 0):
            # control6 already started, change frame rate #
            CTRE.Native.CAN.Send(self.CONTROL_6 | self._deviceNumber, self._cache, 8, self._control6PeriodMs)
        
    """
     * Clear the buffered motion profile in both Talon RAM (bottom), and in the API
     * (top).
    """
    def ClearMotionProfileTrajectories(self):
        #TODO test this, involves semaphores
        #LOCK _mutMotProf
        #clear the top buffer
        self._motProfTopBuffer.Clear()
        #send signal to clear bottom buffer
        frame = self.GetControl16()
        frame = (frame & 0xFFFFFFFFFFFFF0FF) # clear Idx
        self._motProfFlowControl = 0 #match the transmited flow control
        CTRE.Native.CAN.Send(self.CONTROL_6 | self._deviceNumber, frame, 8, 0xFFFFFFFF)

    """
     * Retrieve just the buffer count for the api-level (top) buffer.
     * This routine performs no CAN or data structure lookups, so its fast and ideal
     * if caller needs to quickly poll the progress of trajectory points being
     * emptied into Talon's RAM. Otherwise just use GetMotionProfileStatus.
     * @return number of trajectory points in the top buffer.
    """
    def GetMotionProfileTopLevelBufferCount(self):
        #TODO test this, involves semaphores
        #LOCK _mutMotProf
        retval = self._motProfTopBuffer.GetNumTrajectories()
        return retval

    """
     * Retrieve just the buffer full for the api-level (top) buffer.
     * This routine performs no CAN or data structure lookups, so its fast and ideal
     * if caller needs to quickly poll. Otherwise just use GetMotionProfileStatus.
     * @return number of trajectory points in the top buffer.
    """
    def IsMotionProfileTopLevelBufferFull(self):
        #TODO test this, involves semaphores
        #LOCK _mutMotProf
        if(self._motProfTopBuffer.GetNumTrajectories() >= self.kMotionProfileTopBufferCapacity):
            return True
        return False

    
    """
     * Push another trajectory point into the top level buffer (which is emptied
     * into the Talon's bottom buffer as room allows).
     * @param targPos  servo position in native Talon units (sensor units).
     * @param targVel  velocity to feed-forward in native Talon units (sensor units
     *                 per 100ms).
     * @param profileSlotSelect  which slot to pull PIDF gains from.  Currently
     *                           supports 0 or 1.
     * @param timeDurMs  time in milliseconds of how long to apply this point.
     * @param velOnly  set to nonzero to signal Talon that only the feed-foward
     *                 velocity should be used, i.e. do not perform PID on position.
     *                 This is equivalent to setting PID gains to zero, but much
     *                 more efficient and synchronized to MP.
     * @param isLastPoint  set to nonzero to signal Talon to keep processing this
     *                     trajectory point, instead of jumping to the next one
     *                     when timeDurMs expires.  Otherwise MP executer will
     *                     eventually see an empty buffer after the last point
     *                     expires, causing it to assert the IsUnderRun flag.
     *                     However this may be desired if calling application
     *                     never wants to terminate the MP.
     * @param zeroPos  set to nonzero to signal Talon to "zero" the selected
     *                 position sensor before executing this trajectory point.
     *                 Typically the first point should have this set only thus
     *                 allowing the remainder of the MP positions to be relative to
     *                 zero.
     * @return CTR_OKAY if trajectory point push ok. CTR_BufferFull if buffer is
     *         full due to kMotionProfileTopBufferCapacity.
    """
    def PushMotionProfileTrajectory(self, targPos, targVel, profileSlotSelect, timeDurMs, velOnly, isLastPoint, zeroPos):
        self.ReactToMotionProfileCall()
        b0 = 0
        b1 = 0
        if(zeroPos != 0):
            b0 = (b0 | 0x40)
        if(velOnly != 0):
            b0 = (b0 | 0x04)
        if(isLastPoint != 0):
            b0 = (b0 | 0x08)
        if(profileSlotSelect != 0):
            b0 = (b-0 | 0x80)

        if(timeDurMs < 0):
            timeDurMs = 0
        elif(timeDurMs > 255):
            timeDurMs = 255
            
        #TODO: test bytes are properly assigned
        b2 = (0xFF & timeDurMs)
        b3 = (0xFF & (targVel >> 0x08))
        b4 = (0xFF & (targVel & 0xFF))
        b5 = (0xFF & (targPos >> 0x10))
        b6 = (0xFF & (targPos >> 0x08))
        b7 = (0xFF & (targPos & 0xFF))

        traj = 0
        traj = (traj | b7)
        traj = (traj << 8)
        traj = (traj | b6)
        traj = (traj << 8)
        traj = (traj | b5)
        traj = (traj << 8)
        traj = (traj | b4)
        traj = (traj << 8)
        traj = (traj | b3)
        traj = (traj << 8)
        traj = (traj | b2)
        traj = (traj << 8)
        traj = (traj | b1)
        traj = (traj << 8)
        traj = (trak | b0)

        #TODO: test semaphore:
        #LOCK (_mutMotProf)
        if(self._motProfTopBuffer.GetNumTrajectories() >= self.kMotionProfileTopBufferCapacity):
            return Codes.CAN_OVERFLOW
        self._motProfTopBuffer.Push(traj)

        return Codes.CAN_OK
    
    """
     * Increment our flow control to manage streaming to the Talon.
     * f(x) = { 1,   x = 15,
     *          x+1,  x < 15
     *        }
    """
    def MotionProf_IncrementSync(self, idx):
        val1 = 0
        if(idx >= 15):
            val1 = 1
        return val1 + ((idx + 1) & 0xF)

    """
     * Update the NextPt signals inside the control frame given the next pt to send.
     * @param control pointer to the CAN frame payload containing control6.  Only
     * the signals that serialize the next trajectory point are updated from the
     * contents of newPt.
     * @param newPt point to the next trajectory that needs to be inserted into
     *        Talon RAM.
    """
    def CopyTrajPtIntoControl(self, ref control, newPt):
        control &= 0x0000000000000F30
        control |= 0xFFFFFFFFFFFFF0CF & newPt

    """
     * Caller is either pushing a new motion profile point, or is
     * calling the Process buffer routine.  In either case check our
     * flow control to see if we need to start sending control6.
    """
    def ReactToMotionProfileCall(self):
        if(self._motProfFlowControl < 0):
            """
             * we have not yet armed the periodic frame.  We do this lazilly to
             * save bus utilization since most Talons on the bus probably are not
             * MP'ing.
            """
            self.ClearMotionProfileTrajectories() #this moves flow control so only fires once if ever
            
    """
     * This must be called periodically to funnel the trajectory points from the
     * API's top level buffer to the Talon's bottom level buffer.  Recommendation
     * is to call this twice as fast as the executation rate of the motion profile.
     * So if MP is running with 20ms trajectory points, try calling this routine
     * every 10ms.  All motion profile functions are thread-safe through the use of
     * a mutex, so there is no harm in having the caller utilize threading.
    """
    def ProcessMotionProfileBuffer(self):
        self.ReactToMotionProfileCall()
        # get the last status frame #
        retval = CTRE.Native.CAN.Receive(self.STATUS_9 | self._deviceNumber, ref self._cache, ref self._len)
        #TODO mutex check
        #LOCK _mutMotProf
        NextID = int((self._cache >> 0x8) & 0xF)
        # calc what we expect to receive #
        if(self._motProfFlowControl == NextID):
            # Talon has completed the last req #
            if(self._motProfTopBuffer.IsEmpty()):
                #nothing to do
                pass
            else:
                # get the latest control frame #
                toFill = self.GetControl16()
                front = self._motProfTopBuffer.Front()
                self.CopyTrajPtIntoControl(ref toFill, front)
                self._motProfTopBuffer.Pop()
                self._motProfFlowControl = self.MotionProf_IncrementSync(self._motProfFlowControl)
                #insert latest flow control
                val = self._motProfFlowControl
                val = (val & 0xF)
                val = (val << 8)
                toFill = (toFill & 0xFFFFFFFFFFFFF0FF)
                toFill = (toFill | val)
                CTRE.Native.CAN.Send(self.CONTROL_6 | self._deviceNumber, toFill, 8, 0xFFFFFFFF)
                
        else:
            #still waiting on talon
            pass

    """
     * Retrieve all status information.
     * Since this all comes from one CAN frame, its ideal to have one routine to
     * retrieve the frame once and decode everything.
     * @param [out] flags  bitfield for status bools. Starting with least
     *        significant bit: IsValid, HasUnderrun, IsUnderrun, IsLast, VelOnly.
     *
     *        IsValid  set when MP executer is processing a trajectory point,
     *                 and that point's status is instrumented with IsLast,
     *                 VelOnly, targPos, targVel.  However if MP executor is
     *                 not processing a trajectory point, then this flag is
     *                 false, and the instrumented signals will be zero.
     *        HasUnderrun  is set anytime the MP executer is ready to pop
     *                     another trajectory point from the Talon's RAM,
     *                     but the buffer is empty.  It can only be cleared
     *                     by using SetParam(eMotionProfileHasUnderrunErr,0);
     *        IsUnderrun  is set when the MP executer is ready for another
     *                    point, but the buffer is empty, and cleared when
     *                    the MP executer does not need another point.
     *                    HasUnderrun shadows this registor when this
     *                    register gets set, however HasUnderrun stays
     *                    asserted until application has process it, and
     *                    IsUnderrun auto-clears when the condition is
     *                    resolved.
     *        IsLast  is set/cleared based on the MP executer's current
     *                trajectory point's IsLast value.  This assumes
     *                IsLast was set when PushMotionProfileTrajectory
     *                was used to insert the currently processed trajectory
     *                point.
     *        VelOnly  is set/cleared based on the MP executer's current
     *                 trajectory point's VelOnly value.
     *
     * @param [out] profileSlotSelect  The currently processed trajectory point's
     *        selected slot.  This can differ in the currently selected slot used
     *        for Position and Velocity servo modes.
     * @param [out] targPos The currently processed trajectory point's position
     *        in native units.  This param is zero if IsValid is zero.
     * @param [out] targVel The currently processed trajectory point's velocity
     *        in native units.  This param is zero if IsValid is zero.
     * @param [out] topBufferRem The remaining number of points in the top level
     *        buffer.
     * @param [out] topBufferCnt The number of points in the top level buffer to
     *        be sent to Talon.
     * @param [out] btmBufferCnt The number of points in the bottom level buffer
     *        inside Talon.
     * @return CTR error code
    """  
    def GetMotionProfileStatus(self, out flags, out profileSlotSelect, out targPos, out targVel, out topBufferRem, out topBufferCnt, out btmBufferCnt, out outputEnable):
        # get the latest status frame #
        int retval = CTRE.Native.CAN.Receive(self.STATUS_9 | self._deviceNumber, ref self._cache, ref self._len)

        # clear signals in case we never received an update, caller should check return #
        flags = 0
        profileSlotSelect = 0
        targPos = 0
        targVel = 0
        btmBufferCnt = 0

        # these signals are always available #
        topBufferCnt = self._motProfTopBuffer.GetNumTrajectories()
        topBufferRem = self.kMotionProfileTopBufferCapacity - self._motProfTopBuffer.GetNumTrajectories()

        # TODO: make enums or make a better method prototype #
        if((self._cache & 0x01) > 0):
            flags = (flags | self.kMotionProfileFlag_ActTraj_IsValid)
        if((self._cache & 0x40) > 0):
            flags = (flags | self.kMotionProfileFlag_HasUnderrun)
        if((self._cache & 0x80) > 0):
            flags = (flags | self.kMotionProfileFlag_IsUnderrun)
        if((self._cache & 0x08) > 0):
            flags = (flags | self.kMotionProfileFlag_ActTraj_IsLast)
        if((self._cache & 0x04) > 0):
            flags = (flags | self.kMotionProfileFlag_ActTraj_VelOnly)

        # TODO: check byte logic
        btmBufferCnt = 0xFF & (self._cache >> 0x10)

        targVel = 0xFF & (self._cache >> 0x18)
        targVel = (targVel << 8)
        targVel = (targVel | ((self._cache >> 0x20) & 0xFF))

        targPos = 0xFF & (self._cache >> 0x28)
        targPos = (targPos << 8)
        targPos = (targPos | ((self._cache >> 0x30) & 0xFF))
        targPos = (targPos << 8)
        targPos = (targPos | ((self._cache >> 0x38) & 0xFF))

        if((self._cache & 0x02) > 0):
            profileSlotSelect = 1
        else:
            profileSlotSelect = 0

        outputEnable = ((self._cache >> 4) &0x3)
        # decode output enable
        if((outputEnable == self.kMotionProf_Disabled) or (outputEnable == self.kMotionProf_Enable) or (outputEnable == self.kMotionProf_Hold)):
            pass
        else:
            # do not allow invalid values for sake of user facing enum types
            outputEnable = self.kMotionProf_Disabled

        return retval

    ##------------------------ auto generated ------------------------------------##
    """
     * This API is optimal since it uses the fire-and-forget CAN interface.
     * These signals should cover the majority of all use cases.
    """
    def GetFault_OverTemp(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 52)
        param = ((L & 1) > 0)
        return retval

    def GetFault_UnderVoltage(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 51)
        param = ((L & 1) > 0)
        return retval

    def GetFault_ForLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 50)
        param = ((L & 1) > 0)
        return retval

    def GetFault_RevLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 49)
        param = ((L & 1) > 0)
        return retval

    def GetFault_HardwareFailure(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 48)
        param = ((L & 1) > 0)
        return retval

    def GetFault_ForSoftLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 28)
        param = ((L & 1) > 0)
        return retval

    def GetFault_RevSoftLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 27)
        param = ((L & 1) > 0)
        return retval

    def GetStckyFault_OverTemp(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 53)
        param = ((L & 1) > 0)
        return retval

    def GetStckyFault_UnderVoltage(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 52)
        param = ((L & 1) > 0)
        return retval

    def GetStckyFault_ForLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 51)
        param = ((L & 1) > 0)
        return retval

    def GetStckyFault_RevLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 50)
        param = ((L & 1) > 0)
        return retval

    def GetStckyFault_ForSoftLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 49)
        param = ((L & 1) > 0)
        return retval

    def GetStckyFault_RevSoftLim(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 48)
        param = ((L & 1) > 0)
        return retval

    def GetAppliedThrottle(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 24)
        L = 0xFF & (self._cache >> 32)
        H = (H & 0x7)
        L = (L & 0xFF)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 11))
        raw = (raw >> (32 - 11))
        param = int(raw)
        return retval

    def GetCloseLoopErr(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0)
        M = 0xFF & (self._cache >> 8)
        L = 0xFF & (self._cache >> 16)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | M)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 24))
        raw = (raw >> (32 - 24))
        param = int(raw)
        return retval

    def GetFeedbackDeviceSelect(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 40)
        L = 0xFF & (self._cache >> 48)
        H = (H & 0x1F)
        L = (L & 0x0)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)

        #TODO come up with an equivalent expression
        raw = (raw >> 9)
        param = int(raw)
        return retval 

    def GetModeSelect(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 40)
        L = 0xFF & (self._cache >> 48)
        H = (H & 0x1)
        L = (L & 0xE0)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)

        #TODO come up with an equivalent expression
        raw = (raw >> 5)
        param = int(raw)
        return retval 

    def GetLimitSwitchEn(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 40)
        L = 0xFF & (self._cache >> 48)
        H = (H & 0xFF)
        L = (L & 0xE0)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)

        #TODO come up with an equivalent expression
        raw = (raw >> 13)
        param = int(raw)
        return retval 

    def GetLimitSwitchClosedFor(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 31)
        param = ((L & 1) > 0)
        return retval

    def GetLimitSwitchClosedRev(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_1 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 30)
        param = ((L & 1) > 0)
        return retval

    def GetSensorPosition(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0)
        M = 0xFF & (self._cache >> 8)
        L = 0xFF & (self._cache >> 16)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | M)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 24))
        raw = (raw >> (32 - 24))
        param = int(raw)
        return retval 

    def GetSensorVelocity(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 24)
        L = 0xFF & (self._cache >> 32)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetCurrent(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 40)
        L = 0xFF & (self._cache >> 48)
        H = (H & 0xFF)
        L = (L & 0xC0)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw >> 6)
        param = 0.125 * raw + 0.0
        return retval

    """
     * @param param set to nonzero if brake is enabled.
     *
    """
    def GetBrakeIsEnabled(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_2 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 63)
        param = ((L & 1) > 0)
        return retval

    def GetEncPosition(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_3 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0)
        M = 0xFF & (self._cache >> 8)
        L = 0xFF & (self._cache >> 16)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | M)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 24))
        raw = (raw >> (32 - 24))
        param = int(raw)
        return retval

    def GetEncVel(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_3 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 24)
        L = 0xFF & (self._cache >> 32)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetEncIndexRiseEvents(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_3 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 40)
        L = 0xFF & (self._cache >> 48)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetQuadApin(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_3 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 63)
        param = ((L & 1) > 0)
        return retval

    def GetQuadBpin(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_3 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 62)
        param = ((L & 1) > 0)
        return retval

    def GetQuadIdxpin(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_3 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 61)
        param = ((L & 1) > 0)
        return retval

    def GetAnalogInWithOv(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_4 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0)
        M = 0xFF & (self._cache >> 8)
        L = 0xFF & (self._cache >> 16)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | M)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 24))
        raw = (raw >> (32 - 24))
        param = int(raw)
        return retval

    def GetAnalogInVel(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_4 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 24)
        L = 0xFF & (self._cache >> 32)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetTemp(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_4 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 40)
        raw = 0
        raw = (raw | L)
        param = 0.645161290322581 * raw - 50.0
        return retval

    def GetBatteryV(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_4 | self._deviceNumber, ref self._cache, ref self._len)
        L = 0xFF & (self._cache >> 48)
        raw = 0
        raw = (raw | L)
        param = 0.05 * raw  + 4.0
        return retval

    def GetResetCount(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_5 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0)
        L = 0xFF & (self._cache >> 8)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        param = int(raw)
        return retval

    def GetResetFlags(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_5 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 16)
        L = 0xFF & (self._cache >> 24
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        param = int(raw)
        return retval

    def GetPulseWidthPosition(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_8 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0)
        M = 0xFF & (self._cache >> 8)
        L = 0xFF & (self._cache >> 16)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | M)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 24))
        raw = (raw >> (32 - 24))
        param = int(raw)
        return retval

    def GetPulseWidthVelocity(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_8 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 48)
        L = 0xFF & (self._cache >> 56)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetPulseWidthRiseToRiseUs(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_8 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 32)
        L = 0xFF & (self._cache >> 40)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetFirmVers(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_5 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 32)
        L = 0xFF & (self._cache >> 40)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def SetDemand24(self, param, controlmode):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        H = 0xFF & (param >> 0x10)
        M = 0xFF & (param >> 0x08)
        L = 0xFF & param

        self._cache = (self._cache & (~(0xFF << 16)))
        self._cache = (self._cache & (~(0xFF << 24)))
        self._cache = (self._cache & (~(0xFF << 32)))
        self._cache = (self._cache | (H << 16))
        self._cache = (self._cache | (M << 24))
        self._cache = (self._cache | (L << 32))
        controlmode = (controlmode & 0xF)
        self._cache = (self._cache & ~((0xF) << 52))
        self._cache = (self._cache | (controlmode << 52))

        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetDemand(self, param, controlmode):
        return self.SetDemand(param, controlmode)

    def SetOverrideLimitSwitchEn(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        param = (param & 0x7)
        self._cache = (self._cache & (~(0x7 << 45)))
        self._cache = (self._cache | (param << 45))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetFeedbackDeviceSelect(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        param = (param & 0xF)
        self._cache = (self._cache & (~(0xF << 41)))
        self._cache = (self._cache | (param << 41))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetRevMotDuringCloseLoopEn(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        if(param == false):
            self._cache = (self._cache & (~(1 << 49)))
        else:
            self._cache = (self._cache | (1 << 49))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetOverrideBrakeType(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        param = (param & 0x3)
        self._cache = (self._cache & (~(0x3 << 50)))
        self._cache = (self._cache | (param << 50))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetModeSelect(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        param = (param & 0xF)
        self._cache = (self._cache & (~(0xF << 52)))
        self._cache = (self._cache | (param << 52))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetProfileSlotSelect(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        if(param == false):
            self._cache = (self._cache & (~(1 << 40)))
        else:
            self._cache = (self._cache | (1 << 40))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetRampThrottle(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        L = (param & 0xFF)
        self._cache = (self._cache & (~(0xFF << 56)))
        self._cache = (self._cache | (L << 56))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetRevFeedbackSensor(self, param):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        if(param == false):
            self._cache = (self._cache & (~(1 << 48)))
        else:
            self._cache = (self._cache | (1 << 48))
        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def SetThrottleBump(self, throttleBump):
        retval = CTRE.Native.CAN.GetSendBuffer(self.CONTROL_5 | self._deviceNumber, ref self._cache)
        if(retval != 0):
            return retval
        H3 = (0xFF & ((throttleBump >> 0x08) & 0x7))
        L = (0xFF & throttleBump)

        self._cache = (self._cache & (~(0x07)))
        self._cache = (self._cache & (~(0xFF << 24)))
        self._cache = (self._cache | (H3)
        self._cache = (self._cache | (L << 24))

        CTRE.Native.CAN.Send(self.CONTROL_5 | self._deviceNumber, self._cache, 8, 0xFFFFFFFF)
        return retval

    def GetMotionMagic_ActiveTrajVelocity(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_10 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0x0)
        L = 0xFF & (self._cache >> 0x8)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 16))
        raw = (raw >> (32 - 16))
        param = int(raw)
        return retval

    def GetMotionMagic_ActiveTrajPosition(self, out param):
        retval = CTRE.Native.CAN.Receive(self.STATUS_10 | self._deviceNumber, ref self._cache, ref self._len)
        H = 0xFF & (self._cache >> 0x10)
        M = 0xFF & (self._cache >> 0x18)
        L = 0xFF & (self._cache >> 0x20)
        raw = 0
        raw = (raw | H)
        raw = (raw << 8)
        raw = (raw | M)
        raw = (raw << 8)
        raw = (raw | L)
        #TODO come up with an equivalent expression
        raw = (raw << (32 - 24))
        raw = (raw >> (32 - 24))
        param = int(raw)
        return retval


#CONTINUE FROM LINE 1035

    
class ParamEnum:
    eProfileParamSlot0_P = 1
    eProfileParamSlot0_I = 2
    eProfileParamSlot0_D = 3
    eProfileParamSlot0_F = 4
    eProfileParamSlot0_IZone = 5
    eProfileParamSlot0_CloseLoopRampRate = 6
    eProfileParamSlot1_P = 11
    eProfileParamSlot1_I = 12
    eProfileParamSlot1_D = 13
    eProfileParamSlot1_F = 14
    eProfileParamSlot1_IZone = 15
    eProfileParamSlot1_CloseLoopRampRate = 16
    eProfileParamSoftLimitForThreshold = 21
    eProfileParamSoftLimitRevThreshold = 22
    eProfileParamSoftLimitForEnable = 23
    eProfileParamSoftLimitRevEnable = 24
    eOnBoot_BrakeMode = 31
    eOnBoot_LimitSwitch_Forward_NormallyClosed = 32
    eOnBoot_LimitSwitch_Reverse_NormallyClosed = 33
    eOnBoot_LimitSwitch_Forward_Disable = 34
    eOnBoot_LimitSwitch_Reverse_Disable = 35
    eFault_OverTemp = 41
    eFault_UnderVoltage = 42
    eFault_ForLim = 43
    eFault_RevLim = 44
    eFault_HardwareFailure = 45
    eFault_ForSoftLim = 46
    eFault_RevSoftLim = 47
    eStckyFault_OverTemp = 48
    eStckyFault_UnderVoltage = 49
    eStckyFault_ForLim = 50
    eStckyFault_RevLim = 51
    eStckyFault_ForSoftLim = 52
    eStckyFault_RevSoftLim = 53
    eAppliedThrottle = 61
    eCloseLoopErr = 62
    eFeedbackDeviceSelect = 63
    eRevMotDuringCloseLoopEn = 64
    eModeSelect = 65
    eProfileSlotSelect = 66
    eRampThrottle = 67
    eRevFeedbackSensor = 68
    eLimitSwitchEn = 69
    eLimitSwitchClosedFor = 70
    eLimitSwitchClosedRev = 71
    eSensorPosition = 73
    eSensorVelocity = 74
    eCurrent = 75
    eBrakeIsEnabled = 76
    eEncPosition = 77
    eEncVel = 78
    eEncIndexRiseEvents = 79
    eQuadApin = 80
    eQuadBpin = 81
    eQuadIdxpin = 82
    eAnalogInWithOv = 83
    eAnalogInVel = 84
    eTemp = 85
    eBatteryV = 86
    eResetCount = 87
    eResetFlags = 88
    eFirmVers = 89
    eSettingsChanged = 90
    eQuadFilterEn = 91
    ePidIaccum = 93
    eStatus1FrameRate = 94  # TALON_Status_1_General_10ms_t
    eStatus2FrameRate = 95  # TALON_Status_2_Feedback_20ms_t
    eStatus3FrameRate = 96  # TALON_Status_3_Enc_100ms_t
    eStatus4FrameRate = 97  # TALON_Status_4_AinTempVbat_100ms_t
    eStatus6FrameRate = 98  # TALON_Status_6_Eol_t
    eStatus7FrameRate = 99  # TALON_Status_7_Debug_200ms_t
    eClearPositionOnIdx = 100
    # reserved
    # reserved
    # reserved
    ePeakPosOutput = 104
    eNominalPosOutput = 105
    ePeakNegOutput = 106
    eNominalNegOutput = 107
    eQuadIdxPolarity = 108
    eStatus8FrameRate = 109  # TALON_Status_8_PulseWid_100ms_t
    eAllowPosOverflow = 110
    eProfileParamSlot0_AllowableClosedLoopErr = 111
    eNumberPotTurns = 112
    eNumberEncoderCPR = 113
    ePwdPosition = 114
    eAinPosition = 115
    eProfileParamVcompRate = 116
    eProfileParamSlot1_AllowableClosedLoopErr = 117
    eStatus9FrameRate = 118  # TALON_Status_9_MotProfBuffer_100ms_t
    eMotionProfileHasUnderrunErr = 119
    eReserved120 = 120
    eLegacyControlMode = 121
    eMotMag_Accel = 122
    eMotMag_VelCruise = 123
    eStatus10FrameRate = 124 #// TALON_Status_10_MotMag_100ms_t 


