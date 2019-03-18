from threading import Thread
from multiprocessing import Process
import socket 

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
VERBOSE = False

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
#sock.connect(('192.168.43.25', 22000))  

IP_ADDRESS = "192.168.43.25"
IP_PORT = 22000

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def debug(text):
    if VERBOSE:
        print "Debug:---", text


def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

def adcread1():
    p=Process(target=adcread())
    p.start()

def adcread():
    while True:
        values = [0]*4
        for i in range(4):
            values[i] = mcp.read_adc(i)

        sendCommand('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |'.format(*values)) 

def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sock.sendall(cmd)
    except:
        closeConnection()

def closeConnection():
    global isConnected
    debug("Closing socket")
    sock.close()
    isConnected = False

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debug("Connecting...")
    try:
        sock.connect((IP_ADDRESS, IP_PORT))
    except:
        debug("Connection failed.")
        return False
    adcread1()
    return True

sock = None
isConnected = False

if connect():
    isConnected = True
    print "Connection established"
    while isConnected:
        time.sleep(2)
else:
    print "Connection failed"
    


