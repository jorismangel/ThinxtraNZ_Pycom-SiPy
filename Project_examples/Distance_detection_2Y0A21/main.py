###
###  Thinxtra Pycom SiPy test  - Distance detection application for SiPy with Expansion board
###  Sharp 2Y0A21 sensor used
###  Version 1.0
###  Created by Joris Mangel, Thinxtra Pty.
###  May 4, 2017.

###  Released into the public domain.
###

import time
from machine import ADC


print("Thinxtra Pycom SiPy test - Distance detection")


# Variables and i/o definition
PIN_SENSOR = 'P13' #G5 on expansion board

# Get the distance every 1sec
while(True):

    adc = ADC()
    adc_c = adc.channel(attn=ADC.ATTN_11DB, pin=PIN_SENSOR)
    distance = adc_c()
    if 4095 > distance >= 2850:
        print("d = 7 to 10cm (", distance ,  ")")
    elif 2850 > distance >= 1610:
        print("d = 10 to 20cm (", distance ,  ")")
    elif 1610 > distance >= 1120:
        print("d = 20 to 30cm (", distance ,  ")")
    elif 1120 > distance >= 930:
        print("d = 30 to 40cm (", distance ,  ")")
    elif 930 > distance >= 800:
        print("d = 40 to 50cm (", distance ,  ")")
    elif 800 > distance >= 620:
        print("d = 50 to 60cm (", distance ,  ")")
    elif 620 > distance >= 560:
        print("d = 60 to 70cm (", distance ,  ")")
    elif 560 > distance >= 500:
        print("d = 70 to 80cm (", distance ,  ")")
    else:
        print("d >80cm or < 7cm(", distance ,  ")")
    time.sleep(1)
