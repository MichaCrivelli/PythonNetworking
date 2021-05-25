import socket
import pickle

image = "Assets/bild.PNG"

own = "192.168.1.107",25000
#own = socket.gethostbyname(socket.getfqdn()),25001

server = '192.168.1.107', 25001

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(own)
print("bound to : " + str(own[0]) + ", " + str(own[1]))

msg = 'Hello World'
data = pickle.dumps(msg)

def sendImage():
    with open(image,"rb") as f:
        l = f.read(2048)
        print("sending image data...")
        while l:
            sock.sendto(l,server)
        print("image data sent")

sendImage()

while True:
    try:
        data, addr = sock.recvfrom(1024)
        if not data:
            break
        else:
            MSG = pickle.loads(data)
            print(MSG)
    except socket.error as e:
        print(e)
        break
