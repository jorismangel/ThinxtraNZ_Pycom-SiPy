from network import Sigfox
import binascii
import socket
#import pycom
#import time

# init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
#print({binascii.hexlify(sigfox.id())})
#print({binascii.hexlify(sigfox.pac())})


# disable the heartbeat led
#pycom.heartbeat(False)

try:
    # create a Sigfox socket
    print("creating socket...")
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
    print("socket created!")

    # make the socket blocking
    print("set blocking to true...")
    s.setblocking(True)
    print("blocking set to true!")

    #configure it as uplink only
    #s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
 
    # configure it as DOWNLINK specified by 'True'
    print("set DOWNLINK mode...")
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
    print("DOWNLINK mode set!")

    # send some bytes and request DOWNLINK
    print("sending bytes...")
    output = s.send(bytes([0x0F]))
    print("bytes sent!")

    # blink LED
    #for cycles in range(3): # stop after 10 cycles
        #pycom.rgbled(0x007f00) # green
        #time.sleep(1)
        # turn off the heartbeat LED
        #pycom.rgbled(0)
        #time.sleep(1)

    # await DOWNLINK message
    print("await DOWNLINK message...")
    input = s.recv(8)
    print(output)
    print("... Downlink response ... ")
    print(binascii.hexlify(input))
    print("DOWNLINK message should have been recvd")

except Exception as e:
    print(e)

finally:
    # close socket
    print("closing socket...")
    s.close()
    print("socket closed!")
