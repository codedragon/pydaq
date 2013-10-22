from PyDAQmx import *
import numpy as np
import time

pumpTaskHandle = TaskHandle()

try:
    DAQmxCreateTask("", byref(pumpTaskHandle))
    DAQmxCreateDOChan(pumpTaskHandle, "Dev1/port0/line0", "", DAQmx_Val_ChanPerLine)

    DAQmxStartTask(pumpTaskHandle)

    pumpWrite = np.zeros(1, dtype=numpy.uint8)
    pumpWrite[0] = 1
    DAQmxWriteDigitalLines(pumpTaskHandle, 1, False, DAQmx_Val_WaitInfinitely, DAQmx_Val_GroupByChannel,
                           pumpWrite, None, None)
    pumpWrite[0] = 0
    time.sleep(.05)
    DAQmxWriteDigitalLines(pumpTaskHandle, 1, False, DAQmx_Val_WaitInfinitely, DAQmx_Val_GroupByChannel,
                           pumpWrite, None, None)
    print "sent reward impulse"

except DAQError as err:
    print "DAQmx Error: %s"%err

finally:
    if pumpTaskHandle:
        DAQmxStopTask(pumpTaskHandle)
        DAQmxClearTask(pumpTaskHandle)

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
