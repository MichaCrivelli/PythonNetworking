import socket
import pickle
import time
import threading

#own = socket.gethostbyname(socket.getfqdn()),25001
server = '192.168.1.107', 25000
own = '192.168.1.107', 25030

class Client:
    connected = False

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(own)
        self.connectToServer()
        #self.sendData()

    def connectToServer(self):
        print("Trying to connect with the server")
        while not Client.connected:
            try:
                self.sock.connect(server)
                print(f"connected to: {own[0]}:{own[1]}")
                Client.connected = True
            except:
                continue

    def sendData(self):
        while True:
            data = b"HelloWorld"
            self.sock.sendall(data)
            print("Sent messsage to server")
            time.sleep(1)

    def listen(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                print("-Got Message from server\n")
cl = Client()
threading.Thread(target=cl.sendData).start()
threading.Thread(target=cl.listen).start()
