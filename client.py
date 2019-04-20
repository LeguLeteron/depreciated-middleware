import socket                   # Import socket module
import letero

s = socket.socket()             # Create a socket object
host = ""  #Ip address that the TCPServer  is there
port = 20000                     # Reserve a port for your service every new transfer wants a new port or you must wait.


try:
    s.connect((host, port))
except OSError:
    port += 1
    s.connect((host, port))

while True:
    send = int(input("Input the type: "))
    if send is letero.MODE_IMAGE or letero.MODE_TEXT:
        break

data = letero.USERAGENT + str(send) + " " + input("Input the data: ")
s.send(data.encode())

with open('received_file.mp3', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s' % data)
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
