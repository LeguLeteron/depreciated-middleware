import socket                   # Import socket module
import letero
import kck
import braille

s = socket.socket()             # Create a socket object
host = ""  #Ip address that the TCPServer is there
port = 20000                     # Reserve a port for your service every new transfer wants a new port or you must wait.
legu = letero.Letero()

try:
    s.connect((host, port))
except OSError:
    port += 1
    s.connect((host, port))

legu.useragent["RequestType"] = input("Input the request type: ")
legu.useragent["Language"] = input("Input the language: ")
legu.useragent["ReturnMode"] = input("Input the return mode: ")
legu.useragent["Data"] = input("Input the data: ")

agent = ""
for key, value in legu.useragent.items():
    agent += "{}/{} ".format(key, value)

data = kck.encrypt(1, 3, agent)
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
