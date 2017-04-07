from network import Sigfox
from machine import Pin
#import binascii
import socket
import pycom
import time
#import os

# Disable the heartbeat led
pycom.heartbeat(False)

# initialize GP17 in gpio mode and make it an input with the pull-up enabled
button = Pin("G17", Pin.IN, pull=Pin.PULL_UP)

#LED blinking
while(button.value()): # leave loop after button click
    pycom.rgbled(0x7f7f00) # yellow
    time.sleep(0.2)
    pycom.rgbled(0x7f0000) # red
    time.sleep(0.2)
    pycom.rgbled(0x007f00) # green
    time.sleep(0.2)
    
# init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
#print({binascii.hexlify(sigfox.id())})
#print({binascii.hexlify(sigfox.pac())})

i=10

try:
    # create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
    #print("socket created!")

    # make the socket blocking
    s.setblocking(True)

    #configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

    # configure it as DOWNLINK specified by 'True'
    #s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

    #send some bytes & blink LED  
    while(True): 
        #send bytes
        pycom.rgbled(0x007f00) # green
        print("payload=", bytes([i]))
        s.send(bytes([i]))
        i=(i+1)%16
        pycom.rgbled(0) # turn off the LED        
        time.sleep(10) # 615 if up to 140 messages per day
        
    pycom.rgbled(0x7f0000) # red

    #print("bytes sent!")
    
    # await DOWNLINK message
    #print("await DOWNLINK message...")
    #input = s.recv(32)
    #print(output)
    #print("... Downlink response ... ")
    #print(binascii.hexlify(input))
    #print("DOWNLINK message should have been recvd")

except Exception as e:
    print("Error: "+e)

finally:
    # close socket
    s.close()
    #print("socket closed!")
