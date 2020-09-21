import os.path
import socket
from threading import Thread
from socketserver import ThreadingMixIn


TCP_IP = socket.gethostbyaddr("ec2-18-192-181-222.eu-central-1.compute.amazonaws.com")[0] 
TCP_PORT = 5000
BUFFER_SIZE = 1024

print('TCP_IP: ',TCP_IP,'TCP_port:',TCP_PORT)

class ClientThread(Thread):

    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread " + ip + ":" + str(port)) #new thread instance constructed

    def run(self):

        print("Receiving File Started") #so here we started getting the file

        filename, fileextension = self.sock.recv(1024).decode().split('.')
        self.sock.send('1'.encode())

        if os.path.exists(filename + '.' + fileextension): #here we received the file filename
            filename = filename + "_copy" #we add new copy
        k = 1
        while os.path.exists(filename + str(k) + '.' + fileextension): k += 1      #increment 
        with open(filename + str(k) + '.' + fileextension, 'wb') as f:
            while True:
                new_chunk = self.sock.recv(1024) #start reading chunks
                if not new_chunk:
                    f.close()
                    print('File has been received') #end of reading file
                    break
                f.write(new_chunk)

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((TCP_IP, TCP_PORT))

while True:
    mySocket.listen(5)
    (conn, (ip,port)) = mySocket.accept(); print("Waiting for connection");
    newthread = ClientThread(ip, port, conn); print("New connection from", (ip, port))
    newthread.start()