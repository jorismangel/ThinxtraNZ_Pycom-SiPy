###
###  Thinxtra Pycom SiPy test  - Test application for SiPy with Expansion board
###  Version 1.1
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


### INIT PHASE ###

print("Thinxtra Pycom SiPy test - not using library")

# Print device firmware and library included on flash
print("Device firmware: ",  os.uname().release)
print("Device /flash/lib: ",  os.listdir('/flash/lib'))

# Disable the heartbeat LED
pycom.heartbeat(False)

# Variables and i/o definition
DELAY_BET_MESS = 20 # Delay between two sigfox messages been sent (min delay)
button = Pin("G17", Pin.IN, pull=Pin.PULL_UP) # Initialize GP17 in gpio mode and make it an input with the pull-up enabled
led = Pin('G16', mode=Pin.OUT, value=1) # Initialize GP18 in gpio mode and make it an output

### END INIT ###


### WAIT BUTTON CLICK ###

# WLED blinking until expansion board button click
print("\nPress expansion board's BUTTON to start...\n")
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
print("Device PAC ",  {binascii.hexlify(sigfox.pac())},  "\n")

try:
    # Create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

    # Make the socket blocking
    s.setblocking(True)


    # FIRST MESSAGE REQUESTS DOWNLINK
    print("DOWNLINK MESSAGE...")

    # Configure it as DOWNLINK specified by 'True'
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

    # Send hello message
    print("Payload sent: hello")
    pycom.rgbled(0xFFC000) # LED yellow
    input = s.send("hello")
    pycom.rgbled(0) # Turn off the LED
    print("Nb bytes sent: ", input) # Number of bytes sent

    # Await DOWNLINK message
    print("Message received: ",  s.recv(32),  "\n")


    # OTHER MESSAGES ALL UPLINK ONLY
    print("UPLINK MESSAGES...")

    # Configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

    # Send some bytes & blink LED
    i=0 # from 0x00 to 0x0F counter
    j=0 # from 0x00 to 0xFF counter
    while(True):
        time.sleep(DELAY_BET_MESS)

        # Send bytes
        print("Payload sent: i=",i, " j=",j)
        pycom.rgbled(0x007f00) # LED green
        input = s.send(bytes([i, j]))
        pycom.rgbled(0) # Turn off the LED
        print("Nb bytes sent: ", input,  "\n") # Number of bytes sent
        i = (i+1)%16
        j = (j+1)%256

except Exception as e:
    # Handle expections here
    pycom.rgbled(0x7f0000) # LED red
    print("Error: ",  e)

finally:
    # Close socket
    s.close()

### END SIGFOX COMMUNICATION ###
