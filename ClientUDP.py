
from socket import *
from multiprocessing import Process
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
VERBOSE = False

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

HOST = '192.168.43.189'
PORT = 22000
BUFSIZE = 1024
ADDR = (HOST,PORT)

udpCliSock = socket(AF_INET,SOCK_DGRAM)

while True:

    values = [0]*4
    for i in range(4):
        values[i] = mcp.read_adc(i)
    udpCliSock.sendto('{0:>4}:{1:>4}:{2:>4}:{3:>4}:'.format(*values),ADDR)
    time.sleep(0.1)
    
udpCliSock.close()