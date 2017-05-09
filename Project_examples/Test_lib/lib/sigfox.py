###
###  Thinxtra Pycom SiPy test  - Library for Sigfox device
###  Version 1.0
###  Created by Joris Mangel, Thinxtra Pty.
###  May 9, 2017.

###  Released into the public domain.
###

from network import Sigfox
import pycom
import socket
import os

class SigfoxLib():

    ### On object creation, define zone
    def __init__(self, zone):
        # Define Zone
        if zone == "RCZ1":
            # Init Sigfox for RCZ1 (Europe, Oman, South Africa)
            self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

        elif zone == "RCZ2":
            # Init Sigfox for RCZ2 (USA, Mexico, Brazil)
            self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)

        elif zone == "RCZ3":
            # Init Sigfox for RCZ3 (Japan)
            self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ3)

        elif zone == "RCZ4":
            # Init Sigfox for RCZ4 (Australia, New Zealand, Singapore, Taiwan, Hong Kong, Colombia, Argentina)
            self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)

        else:
            # Default one to RCZ1
            self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

        # Variables
        self.received_mes = ""


    ### Proint firmware, lib content, ID and PAC
    def print_device_info(self):
        # Print device firmware and library included on flash
        print("Device firmware: ",  os.uname().release)
        print("Device /flash/lib: ",  os.listdir('/flash/lib'))

        # Print device ID and PAC
        print("Device ID: ",  {binascii.hexlify(self.sigfox.id())})
        print("Device PAC ",  {binascii.hexlify(self.sigfox.pac())},  "\n")

    ### Create socket and set UPLINK by default
    def init_com(self):
        # Create a Sigfox socket
        self.s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

        # Make the socket blocking
        self.s.setblocking(True)

        # Default UPLINK
        self.s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
        self.mode = 1

    ### Close socket
    def close_com(self):
        # Close socket
        self.s.close()

    ### Set sending mode to DOWNLINK or UPLINK
    def set_sending_mode(self, mode):
        # Define sending mode UPLINK or DOWNLINK
        if mode == "DOWNLINK":
            # Configure it as DOWNLINK specified by 'True'
            self.s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
            self.mode = 0

        elif mode == "UPLINK":
            # Configure it as UPLINK only
            self.s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
            self.mode = 1

        else:
            # Default UPLINK
            self.s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
            self.mode = 1


    ### Send SIGFOX message
    def send_message(self, message):
        # Send message depending on mode UPLINK or DOWNLINK

        if self.mode == 0:
            # DOWNLINK message
            pycom.rgbled(0xFFC000) # LED yellow
            input = self.s.send(message)
            pycom.rgbled(0) # Turn off the LED
            print("Nb bytes sent: ", input) # Number of bytes sent

            # Await DOWNLINK message
            self.received_mes = self.s.recv(32)
            print("Message received: ",  self.received_mes,  "\n")

        else:
            # UPLINK message
            pycom.rgbled(0x007f00) # LED green
            input = self.s.send(message)
            pycom.rgbled(0) # Turn off the LED
            print("Nb bytes sent: ", input,  "\n") # Number of bytes sent


    ### Get message received by DOWNLOAD
    def get_lastrcvd_message(self):
        return self.received_mes
