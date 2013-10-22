import PyDAQmx as daq
import numpy as np
import time

# set up reward object. sends reward pulse to digital output on daq
reward = daq.Task()

reward.CreateDOChan("Dev1/port0/line0", "", daq.DAQmx_Val_ChanPerLine)
reward.StartTask()
pumpWrite = np.zeros(1, dtype=np.uint8)
pumpWrite[0] = 1
reward.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
                                pumpWrite, None, None)
pumpWrite[0] = 0
time.sleep(.05)
reward.WriteDigitalLines(1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
                                pumpWrite, None, None)
print "sent reward impulse"
#
#try:
#    daq.DAQmxCreateTask("", daq.byref(pumpTaskHandle))
#    daq.DAQmxCreateDOChan(pumpTaskHandle, "Dev1/port0/line0", "", daq.DAQmx_Val_ChanPerLine)
#
#    daq.DAQmxStartTask(pumpTaskHandle)
#
#    pumpWrite = np.zeros(1, dtype=np.uint8)
#    pumpWrite[0] = 1
#    daq.DAQmxWriteDigitalLines(pumpTaskHandle, 1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
#                           pumpWrite, None, None)
#    pumpWrite[0] = 0
#    time.sleep(.05)
#    daq.DAQmxWriteDigitalLines(pumpTaskHandle, 1, False, daq.DAQmx_Val_WaitInfinitely, daq.DAQmx_Val_GroupByChannel,
#                           pumpWrite, None, None)
#    print "sent reward impulse"
#
#except daq.DAQError as err:
#    print "DAQmx Error: %s"%err
#
#finally:
#    if pumpTaskHandle:
#        daq.DAQmxStopTask(pumpTaskHandle)
#        daq.DAQmxClearTask(pumpTaskHandle)

# Stuff for writing to file on other machine?
#pEncode = np.zeros(1, dtype=numpy.uint32)
#pEncodeTaskHandle = TaskHandle()
#
#try:
#    DAQmxCreateTask("",byref(pEncodeTaskHandle))
#    DAQmxCreateDOChan( pEncodeTaskHandle, "Dev1/port2","",DAQmx_Val_ChanForAllLines)
#
#    DAQmxStartTask(pEncodeTaskHandle)
#pEncode[0] = event
#DAQmxWriteDigitalU32(pEncodeTaskHandle, 1, 0, 10.0,
#                     DAQmx_Val_GroupByChannel, pEncode, byref(int32()),
#                     None)
