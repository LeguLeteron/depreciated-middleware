import letero
import socket
import kck
import braille

port = 20000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
try:
    s.bind((host, port))
except OSError:
    port += 1
    s.bind((host, port))
s.listen(5)

legu = letero.Letero()

print("Server started.")


while True:
    conn, addr = s.accept()
    print("Got connnection from {}".format(addr))

    data = conn.recv(1024).decode('utf-8')
    data = kck.decrypt(1, 3, data)
    print("Server received {}".format(data))

    header = data.split()[:len(legu.useragent)]
    realdata = data.split()[len(legu.useragent)-1:]

    if "LeguLeteron" not in header[0]:
        conn.send(letero.MODE_ERROR.encode())
        conn.close()
    if str(letero.MODE_TEXT) in header[1]:
        legu = letero.Letero(text=" ".join(realdata))
        legu.to_tts(legu.text)
    else:
        print(realdata)
        legu = letero.Letero(img=' '.join(realdata))
        legu.to_tts(legu.image_to_text())

    filename = "{name}.{type}".format(name=legu.filename, type=legu.filetype)
    f = open(filename, 'rb')

    while True:
        l = f.read(1024)
        conn.send(l)
        print('Sent ', l)
        if not l:
            break

    f.close()

    print("Done sending")
    conn.close()