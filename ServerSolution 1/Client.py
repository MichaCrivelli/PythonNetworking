import socket,os
import threading
import time
import pickle


class Client:

    sending = False
    queue = []
    connected = False
    sock = None



    def __init__(self):
        self.clientAddress = ('192.168.1.107',25003)
        self.serverAddress = ("192.168.1.107",25000)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Client.sock = self.sock
        self.sock.bind(self.clientAddress)
        print("bound to: ",self.getCleanAddr(self.clientAddress))
        self.connectToServer()

    def getCleanAddr(self,addr):
        ip = addr[0]
        port = addr[1]
        return f"{ip}:{port}"

    def connectToServer(self):
        print("Try to connect to server")
        while not Client.connected:
            try:
                self.sock.connect(self.serverAddress)
                print("connected with: ",self.getCleanAddr(self.serverAddress))
                Client.connected = True
            except:
                continue

    def getFileData(self):
        file = "Update/serverlogic.py"
        f = open(file,"rb")
        data = f.read(1024)
        return data

    def SendingThread(self):
        print("--> Start SendingThread")
        while not Client.sending:
            if len(Client.queue) > 0:
                data = Client.queue[0]
                self.sock.sendall(data)
                Client.queue.remove(Client.queue[0])
                print("sent")

    def SendMessage(self,prefix,Message):
        data = pickle.dumps([prefix,Message])
        Client.queue.append(data)

    def sendServerLogic(self):
        self.SendMessage("FileData",self.getFileData())
        Client.connected = False
        time.sleep(2)
        self.sock.close()
        self.__init__()

    def test(self):
        anz = 0
        while True:
            if Client.connected:
                self.SendMessage("Message","Test")
                if anz == 5:
                    self.sendServerLogic()
                    anz = 0
                time.sleep(1)
                anz += 1


class listenThread(Client):

    def __init__(self):
        print("--> Start listening Thread")
        self.listen()

    def ReceiveData(self):
        if Client.connected:
            data = Client.sock.recv(1024)
            if data:
                data = pickle.loads(data)
                return data
        else:
            return None

    def listen(self):
        while True:
            try:
                data = self.ReceiveData()
                if data:
                    if data[0] == "Message":
                        print(data[1])
            except:
                continue


cl = Client()

sending = threading.Thread(target=cl.SendingThread).start()
sendServerLogic = threading.Thread(target=cl.sendServerLogic).start()
listenThread = threading.Thread(target=listenThread).start()
test = threading.Thread(target=cl.test).start()
