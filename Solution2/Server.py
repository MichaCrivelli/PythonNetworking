import socket, os


ip = "192.168.1.107"
port = 25000

addr = (ip,port)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(addr)
print("bound to ",addr)
sock.listen()
print("listening")

sock, address = sock.accept()
print("connected to ",address)

received = 0

data = sock.recv(1024)
with open("NewAssets/bild.png","wb") as f:
    while data:
        f.write(data)
        received+=1
        data = sock.recv(1024)

print("Saved picture in ",received," peaces")
