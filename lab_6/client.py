import socket, os, sys

TCP_IP = sys.argv[2]
TCP_PORT = int(sys.argv[3])

BUFFER_SIZE = 1024

instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
instance.connect((TCP_IP, TCP_PORT))

filename = sys.argv[1]
f = open(filename, 'rb')
instance.send(filename.encode())

check = instance.recv(1)
cur_size = 0

statinfo = os.stat(filename)

print("File sending process started:")

last_progress = 0
#print(statinfo.st_size)
while True:
    l = f.read(BUFFER_SIZE)
    cur_size += BUFFER_SIZE * 2
    #print(cur_size)
    cur_progress = min(100, cur_size / statinfo.st_size * 100)

    if last_progress < cur_progress - 2:
        print("Current progress is -----------------" + str(int(cur_progress)) + "%")
        last_progress = cur_progress
    if l:
        instance.send(l)
        l = f.read(BUFFER_SIZE)
    if not l:
        f.close()
        instance.close()
        break

print('File sent successfully')
instance.close()
print('Socket connection closed')