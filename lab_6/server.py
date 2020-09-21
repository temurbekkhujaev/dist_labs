import socket
import os.path
from threading import Thread
from socketserver import ThreadingMixIn

TCP_IP = 'localhost'
# TCP_IP = socket.gethostbyaddr(
#     "My AWS platform")[0]
TCP_PORT = 60011
BUFFER_SIZE = 1024

print('TCP_IP=', TCP_IP)
print('TCP_PORT=', TCP_PORT)


class ClientThread(Thread):

    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock

        print("New thread started for " + ip + ":" + str(port))

    def run(self):
        print("Getting name of the file")

        name, ext = self.sock.recv(1024).decode().split('.')

        self.sock.send('1'.encode())

        if os.path.exists(name + '.' + ext):
            name = name + "_copy"

        k = 1

        while os.path.exists(name + str(k) + '.' + ext):
            k += 1

        with open(name + str(k) + '.' + ext, 'wb') as f:
            print('file opened')

            while True:
                print('receiving data...')
                data = self.sock.recv(1024)
                print('data=%s', data)

                if not data:
                    f.close()
                    print('file close')
                    break
                # write data to a file
                f.write(data)


tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsocket.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsocket.listen(5)

    print("Waiting for incoming connections...")

    (conn, (ip, port)) = tcpsocket.accept()

    print('Got connection from ', (ip, port))

    new_thread = ClientThread(ip, port, conn)
    new_thread.start()

    threads.append(new_thread)

for t in threads:
    t.join()