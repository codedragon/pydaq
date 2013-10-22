import PyDAQmx as daq
import numpy as np
import time

class GiveReward(daq.Task):
    def __init__(self):
        daq.Task.__init__(self)
        self.pulse = np.zeros(1, dtype = np.uint8)
        self.CreateDOChan("Dev1/port0/line0", "", daq.DAQmx_Val_ChanPerLine)
        self.StartTask()

    def pumpout(self):
        self.pulse[0] = 1
        self.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
                                 self.pulse, None, None)
        self.pulse[0] = 0
        time.sleep(.05)
        self.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
                                 self.pulse, None, None)
        print "sent reward impulse"

#task = GiveReward()
#task.pumpout()

# set up reward object. sends reward pulse to digital output on daq
#reward = daq.Task()
#
#reward.CreateDOChan("Dev1/port0/line0", "", daq.DAQmx_Val_ChanPerLine)
##reward.CreateDOChan("sim-pci-6221/port0/line0", "", daq.DAQmx_Val_ChanPerLine)
#reward.StartTask()
#def giveReward(self):
#    reward.pumpWrite = np.zeros(1, dtype=np.uint8)
#    reward.pumpWrite[0] = 1
#    reward.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
#                             reward.pumpWrite, None, None)
#    reward.pumpWrite[0] = 0
#    time.sleep(.05)
#    reward.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
#                             reward.pumpWrite, None, None)
#    print "sent reward impulse"
#
## set up eog
#eogSampRate = 240
#eogSampsPerChanToAcquire = 1
#eog = daq.Task()
#eogData = np.zeros(2)
#
#eog.CreateAIVoltageChan("Dev1/ai3", "", daq.DAQmx_Val_RSE, -5.0, 5.0, daq.DAQmx_Val_Volts, None)
#eog.CreateAIVoltageChan("Dev1/ai4", "", daq.DAQmx_Val_RSE, -5.0, 5.0, daq.DAQmx_Val_Volts, None)
#eog.CfgSampClkTiming("", eogSampRate, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, eogSampsPerChanToAcquire)
#
#eog.ReadAnalogF64(1,10.0,daq.DAQmx_Val_GroupByScanNumber,eogData,2,daq.byref(daq.read),None)
#eog.StartTask()
#eog.StopTask()