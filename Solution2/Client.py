import socket,os

ip = '192.168.1.107'
port = 25001

addr = (ip,port)

server =("192.168.1.102",25000)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(addr)

sock.connect(server)
print("connected to server")


print("sending image ...")
image = "Assets/bild.png"

with open("Assets/Musik.mp3","rb") as f:
    imgData = f.read()
    sock.sendall(imgData)
print("Done")
