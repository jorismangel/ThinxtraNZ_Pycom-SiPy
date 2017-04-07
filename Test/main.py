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
    pycom.rgbled(0x9400D3) 
    time.sleep(0.2)
    pycom.rgbled(0x4B0082) 
    time.sleep(0.2)
    pycom.rgbled(0x0000FF) 
    time.sleep(0.2)
    pycom.rgbled(0x00FF00) 
    time.sleep(0.2)
    pycom.rgbled(0xFFFF00) 
    time.sleep(0.2)
    pycom.rgbled(0xFF7F00) 
    time.sleep(0.2)
    pycom.rgbled(0xFF0000) 
    time.sleep(0.2)

pycom.rgbled(0) # turn off the LED    
    
# init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
#print({binascii.hexlify(sigfox.id())})
#print({binascii.hexlify(sigfox.pac())})

i=0

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
        time.sleep(5)
        
        #send bytes
        pycom.rgbled(0x007f00) # green
        print("payload=", i)
        input=s.send(bytes([i]))
        print(input)
        i=(i+1)%16
        pycom.rgbled(0) # turn off the LED        
        
        time.sleep(5) 


    #print("bytes sent!")
    
    # await DOWNLINK message
    #print("await DOWNLINK message...")
    #input = s.recv(32)
    #print(output)
    #print("... Downlink response ... ")
    #print(binascii.hexlify(input))
    #print("DOWNLINK message should have been recvd")

except Exception as e:
    pycom.rgbled(0x7f0000) # red
    print("Error: "+e)

finally:
    # close socket
    s.close()
    #print("socket closed!")
