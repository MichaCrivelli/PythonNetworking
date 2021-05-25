import socket
import pickle

#own = socket.gethostbyname(socket.getfqdn()),25001

filePath = "Assets/bild.png"

server = '192.168.1.107', 25000

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


def getStatus():
    data = pickle.dumps("getStatus")
    sock.sendto(data,server)
    print("asking")
    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            data = pickle.loads(data)
            print("Server is: ",data)
            break

def sendImage():
    image = "Assets/bild.png"
    #ask Server
    data = pickle.dumps("Image")
    sock.sendto(data,server)
    print("asking server for sending image data")
    #wait for reply
    while True:
        data, addr = sock.recvfrom(2048)
        if data:
            data = pickle.loads(data)
            if data == "accepted":
                print("sending image data to server")
                image = open(filePath,"rb")
                imgData = image.read()
                sock.sendto(imgData,server)

    #end

getStatus()
sendImage()
