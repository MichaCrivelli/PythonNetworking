import socket

ip = "192.168.1.107"
port = 25000

serverIp = "192.168.1.123"
serverPort = 25000

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("try to connect to server")
sock.connect((serverIp,serverPort))
