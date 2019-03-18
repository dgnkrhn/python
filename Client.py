
from threading import Thread
import socket, time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

VERBOSE = False
IP_ADDRESS = "192.168.43.25" #Server ip adresi
IP_PORT = 22000

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)
    CLK  = 18
    MISO = 23
    MOSI = 24
    CS   = 25
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def debug(text):
    if VERBOSE:
        print "Debug:---", text

# ------------------------- class Receiver ---------------------------
class Receiver(Thread):
    def run(self):
        debug("Receiver thread started")
        while True:
            try:
                rxData = self.readServerData()
            except:
                debug("Exception in Receiver.run()")
                isReceiverRunning = False
                closeConnection()
                break
        debug("Receiver thread terminated")

    def readServerData(self):
        debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
                if blk != None:
                    debug("Received data block from server, len: " + \
                        str(len(blk)))
                else:
                    debug("sock.recv() returned with None")
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += blk
        print "Data received:", data
# ------------------------ End of Receiver ---------------------

def adcRead():
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
#    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |'.format(*values))
    # Pause for half a second.
    
    x1 = '{0:>4}'.format(*values)
    y1 = '{1:>4}'.format(*values)
    x2 = '{2:>4}'.format(*values)
    y2 = '{3:>4}'.format(*values)

    print(x1, y1, x2, y2)
 
    time.sleep(1)

def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sock.sendall(cmd + "\0")
    except:
        debug("Exception in sendCommand()")
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
    startReceiver()
    return True

sock = None
isConnected = False

if connect():
    isConnected = True
    print "Connection established"
    time.sleep(1)
    while isConnected:
        print "Sending command: go..."
        sendCommand("deneme")
        time.sleep(2)
else:
    print "Connection to %s:%d failed" % (IP_ADDRESS, IP_PORT)
print "done"    