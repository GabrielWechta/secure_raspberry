import pyshark
capture = pyshark.LiveCapture(interface='wlo1')

capture.sniff(timeout=10)
print(capture)