import pydaq

send_events = pydaq.OutputEvents()
send_strobe = pydaq.StrobeEvents()
send_events.send_signal(200)
print 200
send_strobe.send_signal()
for i in range(5):
    print(0 + i)
    send_events.send_signal(0 + i)
    send_strobe.send_signal()
for i in range(1, 6):
    print(i * 10)
    send_events.send_signal(i * 10)
    send_strobe.send_signal()
for i in range(0, 251, 25):
    print(i)
    send_events.send_signal(i)
    send_strobe.send_signal()
send_events.close()
send_strobe.close()