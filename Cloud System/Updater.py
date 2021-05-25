import socket
import pickle
import ast

def readSaveFile():
    with open("save.txt","r") as f:
        save = f.read()
        save = ast.literal_eval(save)
        addr = save["Server"]["addr"]
        return addr

serverAddress = readSaveFile()

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Trying to Connnect")
while True:
    try:
        sock.connect(serverAddress)
        print("connected")
        break
    except:
        continue

msg = b"updater"
sock.send(msg)

while True:
    data = sock.recv(1024)
    if data:
        if data == "restart":
            print("RESTART SERVER")
    else:
        break
