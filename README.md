# ThinxtraNZ_Pycom-SiPy

## Synopsis

Sample Code for the Pycom SiPy.
A way to get started with Sigfox, the devkit SiPy boasts a full suite of features and accessories to empower anyone to set up an IoT solution, even with very little hardware experience.

Thinxtra is a Sigfox operator based on Australia/NZ/HK.
The aim of this project is to perform some tests on Pycom SiPy using Thinxtra's Sigfox network.

## Code Example

Send a Sigfox message

-UPLINK only:
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

# configure it as uplink
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send hello message
s.send("Hello world")
```

-DOWNLINK requested:
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

# configure it as downlink specified by 'True'
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

# send hello message
s.send("Hello world")

# await downlink message
print("Message received: ",  s.recv(32))
```
