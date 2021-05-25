import socket
import pickle

newfilePath = "NewAssets/bild.png"

self = '192.168.1.107',25001

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(self)
print('bound to : ' + str(self[0]) + ", " + str(self[1]))

while True:
    try:
        imgData, addr = sock.recvfrom(2048)
        if not imgData:
            print("No Data")
            break
        else:
            #writing Image
            #imgData = repr(data)
            with open(newfilePath,"wb") as f:
                f.write(imgData)

            #reply
            reply = "got your message"
            reply = pickle.dumps(reply)
            sock.sendto(reply,addr)
    except socket.error as e:
        print(e)
        break
