# -*- coding: utf-8 -*- 
import socket
from threading import Thread
import time

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
                    x1 = veri[3]
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
    if (int(x1) < 500):
        print ('Geri :' + str(500 - int(x1)))

    if (int(x1) > 524):
        print ('İleri :' + str(int(x1) - 524))
    
    if (int(x1) < 524) and (int(x1) > 500):
        print ('Hareketsiz')


if __name__ == "__main__":
    host = '192.168.43.25'
    #host = '192.168.1.5'
    port = 22000
    main = Server(host, port)
    # start listening for clients
    main.listen_for_clients()


