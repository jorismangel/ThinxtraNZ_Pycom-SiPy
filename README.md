# ThinxtraNZ_Pycom-SiPy

## Synopsis

Sample Codes for the Pycom SiPy.
A way to get started with Sigfox, the devkit SiPy boasts a full suite of features and accessories to empower anyone to set up an IoT solution, even with very little hardware experience.

Thinxtra is a Sigfox operator based on Australia/NZ/HK.
The aim of this project is to perform some tests on Pycom SiPy using Thinxtra's Sigfox network.

Thinxtra website: http://www.thinxtra.com.
Pycom documentation: https://docs.pycom.io/pycom_esp32/index.html


## Code Examples

### Project descriptions

#### Test_lib and Test_nolib
* Print device firmware, ID and PAC (original one)
* Wait the user to press button on expansion board and LED blinking
* After press, send a message requesting downlink and display answer
* Loop: Send an uplink message every 10 seconds with 2 counters as payload

#### Temperature_DS18X20
* Using temperature sensor DS18X20
* Get temperature every 2 seconds

#### Distance_detection_2Y0A21
* Using distance detection sensor 2Y0A21
* Get distance every second

### Send a Sigfox message:

**UPLINK only:**

```python
# init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send hello message
s.send("Hello world")
```

**DOWNLINK requested:**

```python
# init Sigfox for RCZ4 (Austrlia/NZ)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)

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
