###
###  Thinxtra Pycom SiPy test  - Test application for SiPy with Expansion board
###  Version 1.0
###  Created by Joris Mangel, Thinxtra Pty.
###  April 13, 2017.
  
###  Released into the public domain.
###

from network import Sigfox
from machine import Pin
import socket
import pycom
import time
import binascii
import os


### INIT phase ###
print("Thinxtra Pycom SiPy test ")

# Print device firmware
print("Device firmware: ",  os.uname().release)

# Disable the heartbeat led
pycom.heartbeat(False)
 
# Initialize GP17 in gpio mode and make it an input with the pull-up enabled
button = Pin("G17", Pin.IN, pull=Pin.PULL_UP)

# Variables
i=0
j=0

### END INIT ###


### WAIT BUTTON CLICK ###

# Wait until button click - LED blinking
while(button.value()):
    pycom.rgbled(0x220B68) 
    time.sleep(0.2)
    pycom.rgbled(0x5B1EC3) 
    time.sleep(0.2)
    pycom.rgbled(0x1EAFBB) 
    time.sleep(0.2)
pycom.rgbled(0)  # Turn off the LED  

### END WAIT BUTTON ###


### SIGFOX COMMUNICATION ###
    
# Init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)

# Print device ID and PAC
print("Device ID: ",  {binascii.hexlify(sigfox.id())})
print("Device PAC ",  {binascii.hexlify(sigfox.pac())})

try:
    # Create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

    # Make the socket blocking
    s.setblocking(True)
    
    
    # FIRST MESSAGE REQUESTS DOWNLINK
    print("\nDOWNLINK MESSAGE...")
    
    # Configure it as DOWNLINK specified by 'True'
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
    
    # Send hello message
    print("Payload sent: hello")
    pycom.rgbled(0x007f00) # LED green
    input = s.send("hello")
    pycom.rgbled(0) # Turn off the LED        
    print("Nb bytes sent: ", input,  "\n") # Number of bytes sent
        
    # Await DOWNLINK message
    print("Message received: ",  s.recv(32))
    
    
    # OTHER MESSAGES ALL UPLINK ONLY
    print("\nUPLINK MESSAGES...")

    # Configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

    # Send some bytes & blink LED  
    while(True): 
        time.sleep(5)
        
        # Send bytes
        print("Payload sent: i=", i, "j=", j)
        pycom.rgbled(0x007f00) # LED green
        input = s.send(bytes([i, j]))
        pycom.rgbled(0) # Turn off the LED        
        print("Nb bytes sent: ", input,  "\n") # Number of bytes sent
        i = (i+1)%16
        j = (j+1)%256
        
        time.sleep(5)

except Exception as e:
    pycom.rgbled(0x7f0000) # LED red
    print("Error: ",  e)

finally:
    # Close socket
    s.close()
    
### END SIGFOX COMMUNICATION ###
