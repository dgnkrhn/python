#! /usr/bin/python
# a simple tcp server
import socket,os
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('192.168.43.25', 22000))  
sock.listen(1)
x=1  
while True:  
    connection,address = sock.accept()
    x=x+1  
    buf = connection.recv(1024)  
    print buf
    print x
    connection.send(buf)    		
    #connection.close()