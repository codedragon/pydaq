from PyDAQmx import *
import numpy

# testing reading digital input

#Declaration of variable passed by reference
digital_input = Task()
read = int32()
data = numpy.zeros(10, dtype=numpy.uint32)
#data = numpy.zeros((1000,), dtype=numpy.float64)

#DAQ Configuration Code
digital_input.CreateDIChan("Dev1/port1/line1","",DAQmx_Val_ChanForAllLines)

#DAQmx Start Code
digital_input.StartTask()
print "Acquiring samples continuously. Press Ctrl+C to interrupt\n"

#DAQmx Read Code
digital_input.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data, 1000, byref(read), None)
print "Acquired %d points"%read.value
