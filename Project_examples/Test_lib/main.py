###
###  Thinxtra Pycom SiPy test  - Test application for SiPy with Expansion board
###  Version 2.0
###  Created by Joris Mangel, Thinxtra Pty.
###  April 13, 2017.

###  Released into the public domain.
###

from sigfox import SigfoxLib
from machine import Pin
import time
import pycom


### INIT PHASE ###

print("Thinxtra Pycom SiPy test - using library")

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
sigfox = SigfoxLib(zone="RCZ4")

try:
    # Init Sigfox communication
    sigfox.init_com()
    sigfox.print_device_info()

    # First message requests DOWNLINK
    print("DOWNLINK MESSAGE...")
    sigfox.set_sending_mode("DOWNLINK") # Configure DOWNLINK option
    sigfox.send_message("hello") # Send hello message
    rcvd_msg = sigfox.get_lastrcvd_message() # Last message received after DOWNLINK request

    # Other messages UPLINK
    print("UPLINK MESSAGES...")
    sigfox.set_sending_mode("UPLINK") # Configure UPLINK option

    # Send some bytes & blink LED
    i=0 # from 0x00 to 0x0F counter
    j=0 # from 0x00 to 0xFF counter
    while(True):
        time.sleep(DELAY_BET_MESS)
        print("Payload sent: i=", i, "j=", j)
        sigfox.send_message(bytes([i, j])) # Send hello message
        i = (i+1)%16 # increment i counter
        j = (j+1)%256 # increment j counter

except Exception as e:
    # Handle expections here
    pycom.rgbled(0x7f0000) # LED red
    print("Error: ",  e)

finally:
    # Close Sigfox com
    sigfox.close_com()

### END SIGFOX COMMUNICATION ###
