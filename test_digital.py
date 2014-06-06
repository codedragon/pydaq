import pydaq

send_events = pydaq.OutputEvents()
send_strobe = pydaq.StrobeEvents()
send_events.send_signal(200)
send_strobe.send_signal()
for i in range(5):
    send_events.send_signal(100 + i)
    send_strobe.send_signal()
send_events.close()
send_strobe.close()