import socket
import pickle

serverAddress = ("192.168.1.107",25000)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Trying to Connnect")
while True:
    try:
        sock.connect(serverAddress)
        print("connected")
        break
    except:
        continue

msg = "restart"

sock.sendall(pickle.dumps(msg))
print("sent message")
