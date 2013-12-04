import PyDAQmx as daq
import numpy as np
import time


class GiveReward(daq.Task):
    """Sets up Nidaq board to send a pulse to the reward pump, uses Dev1, port0, line1
    """
    def __init__(self):
        daq.Task.__init__(self)
        self.pulse = np.zeros(1, dtype = np.uint8)
        self.CreateDOChan("Dev1/port0/line0", "", daq.DAQmx_Val_ChanPerLine)

    def pumpOut(self):
        """
        Send signal to the reward pump to trigger a new reward.
        """
        self.StartTask()
        self.pulse[0] = 1
        self.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
                                 self.pulse, None, None)
        self.pulse[0] = 0
        time.sleep(.05)
        self.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
                                 self.pulse, None, None)
        self.StopTask()
        #print "sent reward impulse"


class EOGTask(daq.Task):
    """Collects Voltage representing Eye Position data from the IScan computer.
    Uses Dev1/ai3 and Dev1/ai4 channels
    """
    def __init__(self):
        daq.Task.__init__(self)
        EOGSampRate = 240
        EOGSampsPerChanToAcquire = 1
        self.EOGData = np.zeros(2)
        self.CreateAIVoltageChan("Dev1/ai3", "", daq.DAQmx_Val_RSE, -5.0, 5.0, daq.DAQmx_Val_Volts, None)
        self.CreateAIVoltageChan("Dev1/ai4", "", daq.DAQmx_Val_RSE, -5.0, 5.0, daq.DAQmx_Val_Volts, None)
        self.CfgSampClkTiming("", EOGSampRate, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, EOGSampsPerChanToAcquire)
        self.AutoRegisterEveryNSamplesEvent(daq.DAQmx_Val_Acquired_Into_Buffer, 1, 0)
        self.AutoRegisterDoneEvent(0)
        # set event to false, if a callback is set, it will be set to self.event.
        self.event = False

    def EveryNCallback(self):
        #print 'callback'
        read = daq.int32()
        #print 'read', read
        self.ReadAnalogF64(1, 10.0, daq.DAQmx_Val_GroupByScanNumber, self.EOGData, 2, daq.byref(read), None)
        if self.event:
            self.event(self.EOGData)
        #print 'x,y', self.EOGData[0], self.EOGData[1]
        #print 'okay'
        return 0  # the function should return an integer

    def DoneCallback(self, status):
        #print 'done callback'
        #print 'Status', status.value
        #print 'what'
        return 0  # the function should return an integer

    def SetCallback(self, event):
        self.event = event
