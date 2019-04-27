# -*- coding: utf-8 -*- 
import socket
from threading import Thread
import time
import RPi.GPIO as GPIO          


in1 = 24
in2 = 23
en = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,50)
p.start(7.5)

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)

    def listen_for_clients(self):
        print('Listening...')
        while True:
            client, addr = self.server.accept()
            print(
                'Accepted Connection from: ' + str(addr[0]) + ':' + str(addr[1])
            )
            Thread(target=self.handle_client, args=(client, addr)).start()

    def handle_client(self, client_socket, address):
        size = 1024
        while True:
            try:
                data = client_socket.recv(size)
                
                if 'q^' in data.decode():    
                    print('Received request for exit from: ' + str(
                        address[0]) + ':' + str(address[1]))
                    break

                else:
                    # send getting after receiving from client
                    client_socket.sendall('Welcome to server'.encode())

                    veri = data.encode().split(":")
                    #print(veri)
                    global x1
                    global x2
                    x1 = veri[1]
                    x2 = veri[3]
                    #y1 = veri[1]
                    #x2 = veri[2]
                    #y2 = veri[3]
                    #print x1
                    donusturme()                    


            except socket.error:
                client_socket.close()
                return False

        client_socket.sendall(
            'Received request for exit. Deleted from server threads'.encode()
        )

        # send quit message to client too
        client_socket.sendall(
            'q'.encode()
        )
        client_socket.close()

def donusturme():
    

    if (int(x2) < 500):
        #p.ChangeDutyCycle( ( ( 500.0 - float(x2) ) / 110.0 ) + 7.5 )
        #print ( ( ( 500.0 - float(x2) ) / 110.0 ) + 7.5 )

        p.ChangeDutyCycle( ( ( 500.0 - float(x2) ) * 0.01 ) + 7.5 )
        #print( ( ( 500.0 - float(x2) ) * 0.01 ) + 7.5 )

    if (int(x2) > 524):
        #p.ChangeDutyCycle( 7.5 - ( ( float(x2) - 524.0 ) / 100.0 ) ) 
        #print ( 7.5 - ( ( float(x2) - 524.0 ) / 100.0 ) ) 

        p.ChangeDutyCycle( 7.5 - ( ( float(x2) - 524.0 ) * 0.01 ) )
        #print( 7.5 - ( ( float(x2) - 524.0 ) * 0.01 ) )
    
    if (int(x2) < 524) and (int(x2) > 500):

        p.ChangeDutyCycle(7.5)
         


if __name__ == "__main__":
    host = '192.168.43.189'
    #host = '192.168.1.5'
    port = 22000
    main = Server(host, port)
    # start listening for clients
    main.listen_for_clients()


