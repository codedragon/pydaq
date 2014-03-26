import PyDAQmx as Daq
import numpy as np
import time
# need to refactor. inconsistent naming. started adapting camelcase
# as used in pydaqmx, but then out of habit switched to underscores.
# And pumpOut borrowed name from Kiril's code, and it doesn't fit with
# either naming convention...


class GiveReward(Daq.Task):
    """Sets up Nidaq board to send a pulse to the reward pump, uses Dev1, port0, line1
    """
    def __init__(self):
        Daq.Task.__init__(self)
        self.pulse = np.zeros(1, dtype = np.uint8)
        self.CreateDOChan("Dev1/port0/line0", "", Daq.DAQmx_Val_ChanPerLine)

    def pumpOut(self):
        """
        Send signal to the reward pump to trigger a new reward.
        """
        self.StartTask()
        self.pulse[0] = 1
        self.WriteDigitalLines(1, False, Daq.DAQmx_Val_WaitInfinitely,
                               Daq.DAQmx_Val_GroupByChannel,
                               self.pulse, None, None)
        self.pulse[0] = 0
        time.sleep(.05)
        self.WriteDigitalLines(1, False, Daq.DAQmx_Val_WaitInfinitely,
                               Daq.DAQmx_Val_GroupByChannel,
                               self.pulse, None, None)
        self.StopTask()
        #print "sent reward impulse"


class EOGTask(Daq.Task):
    """Collects Voltage representing Eye Position data from the IScan computer.
    Uses Dev1/ai3 and Dev1/ai4 channels
    """
    def __init__(self):
        Daq.Task.__init__(self)
        EOGSampRate = 240
        EOGSampsPerChanToAcquire = 1
        self.EOGData = np.zeros(2)
        self.CreateAIVoltageChan("Dev1/ai3", "", Daq.DAQmx_Val_RSE,
                                 -5.0, 5.0, Daq.DAQmx_Val_Volts, None)
        self.CreateAIVoltageChan("Dev1/ai4", "", Daq.DAQmx_Val_RSE,
                                 -5.0, 5.0, Daq.DAQmx_Val_Volts, None)
        self.CfgSampClkTiming("", EOGSampRate, Daq.DAQmx_Val_Rising,
                              Daq.DAQmx_Val_ContSamps, EOGSampsPerChanToAcquire)
        self.AutoRegisterEveryNSamplesEvent(Daq.DAQmx_Val_Acquired_Into_Buffer, 1, 0)
        self.AutoRegisterDoneEvent(0)
        # set event to false, if a callback is set, it will be set to self.event.
        self.event = False

    def EveryNCallback(self):
        #print 'callback'
        read = Daq.int32()
        #print 'read', read
        self.ReadAnalogF64(1, 10.0, Daq.DAQmx_Val_GroupByScanNumber,
                           self.EOGData, 2, Daq.byref(read), None)
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


class OutputEvents(Daq.Task):
    """ Sends out signals of events to Plexon or Blackrock so we can line up data.
    Send strobe after event code.
    """
    def __init__(self):
        Daq.Task.__init__(self)
        self.encode = np.zeros(1, dtype=np.uint32)
        self.strobeOn = np.ones(1, dtype=np.uint32)
        self.strobeOff = np.zeros(1, dtype=np.uint32)
        self.CreateDOCChan("Dev1/port1", "", Daq.DAQmx_Val_ChanForAllLines)
        self.CreateDOCChan("Dev1/port2", "", Daq.DAQmx_Val_ChanForAllLines)

    def send_signal(self, event):
        read = Daq.int32()
        self.encode = event[0]
        self.StartTask()
        self.WriteDigitalU32(1, 0, 10.0, Daq.DAQmx_Val_GroupByChannel,
                             self.encode, Daq.byref(read), None)
        self.WriteDigitalU32(1, 0, 10.0, Daq.DAQmx_Val_GroupByChannel,
                             self.strobeOn, Daq.byref(read), None)
        self.WriteDigitalU32(1, 0, 10.0, Daq.DAQmx_Val_GroupByChannel,
                             self.strobeOff, Daq.byref(read), None)
        self.stopTask()


class OutputAvatarPos(Daq.Task):
    """ Sends out avatar position to Plexon or Blackrock so we can analyze primarily with that data.
    Need to make this a callback
    """
    def __init__(self):
        Daq.Task.__init__(self)
        self.xPosData = np.zeros(1, dtype=np.float64)
        self.CreateAOVoltageChan("Dev1/ao0", "", -10, 10, Daq.DAQmx_Val_Volts, None)
        self.yPosData = np.zeros(1, dtype=np.float64)
        self.CreateAOVoltageChan("Dev1/ao1", "", -10, 10, Daq.DAQmx_Val_Volts, None)

    def send_signal(self, event):
        read = Daq.int32()
        self.StartTask()
        self.WriteDigitalLines(1, 0, 10.0, Daq.DAQmx_Val_GroupByChannel,
                               event[0], Daq.byref(read), None)
        self.stopTask()