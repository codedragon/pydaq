from PyDAQmx import *
import numpy


# Quick test that object works and we get data from IScan computer,
# read 1000 data points, and dump it to the terminal
analog_input = Task()
read = int32()
data = numpy.zeros((1000,), dtype=numpy.float64)

# DAQmx Configure Code
# we use Dev1/ai3 and Dev1/ai4 for eye tracking computer
analog_input.CreateAIVoltageChan("Dev1/ai4","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
analog_input.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

# DAQmx Start Code
analog_input.StartTask()

# DAQmx Read Code
analog_input.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

print "Acquired %d points"%read.value
print data