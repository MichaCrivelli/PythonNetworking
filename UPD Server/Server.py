import socket
import pickle

newfilePath = "NewAssets/bild.png"

self = '192.168.1.107',25000

status = "online"

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.bind(self)
print("bound to: ",self)

while True:
    data,addr = sock.recvfrom(1024)
    if data:
        data = pickle.loads(data)
        if data == "getStatus":
            sock.sendto(pickle.dumps(status),addr)
            print("sent status to: ",addr)
        elif data == "Image":
            print("getting image data from: ",addr)
            sock.sendto(pickle.dumps("accepted"),addr)
            while True:
                data, addr = sock.recvfrom(1024)
                if type(data) == bytes:
                    data = pickle.loads(data)
                    print(data)
                else:
                    print("got image data")
