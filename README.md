# ThinxtraNZ_Pycom-SiPy

## Synopsis

Thinxtra is a Sigfox operator based on Australia/NZ/HK.
The aim of this project is to perform some tests on Pycom SiPy using Thinxtra's Sigfox network.

## Code Example

Send a Sigfox message:
```python
# init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)

# print device ID and PAC
print({binascii.hexlify(sigfox.id())})
print({binascii.hexlify(sigfox.pac())})

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

#configure it as uplink
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

#send bytes
s.send("Hello world")
```
