###
###  Thinxtra Pycom SiPy test  - Temperature aquisition application for SiPy with Expansion board
###  DS18X20 temp sensor used
###  Version 1.0
###  Created by Peroze Irani, Thinxtra Pty.
###  Updated by Joris Mangel, Thinxtra Pty.
###  May 9, 2017.

###  Released into the public domain.
###

import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire


print("Thinxtra Pycom SiPy test - Temperature sensor")

# Sensor input
ow = OneWire(Pin('P8'))
temp = DS18X20(ow)

# Get temperature
while(True):
   print(temp.read_temp_async())
   time.sleep(1)
   temp.start_convertion()
   time.sleep(1)
