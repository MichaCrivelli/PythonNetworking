import socket
import pickle
import time
import threading

#own = socket.gethostbyname(socket.getfqdn()),25001
server = '26.52.199.234', 25001
own = '26.52.199.234', 25000

class Client:
    connected = False
    listening = True
    sending = True
    sendingQueue = []

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(own)
        self.filename = "Update/NewServerlogic.py"
        Client.send = True
        self.connectToServer()
        #self.sendData()

    def testInput(self):
        try:
            data = self.sock.recv(1024)
            data = pickle.loads(data)
            return data
        except:
            return None

    def connectToServer(self):
        print(f"Trying to connect with the server: {own[0]}:{own[1]}")
        while not Client.connected:
            try:
                self.sock.connect(server)
                print(f"connected to: {own[0]}:{own[1]}")
                Client.connected = True
                Client.listening = True
                Client.sending = True
            except:
                continue

    def testConnection(self):
        print("testing connection")
        try:
            data = self.sock.recv(1024)
            if data:
                return True
        except:
                return False

    def addToQueue(self,item):
        Client.sendingQueue.append(item)

    def sendMessage(self,Message,pickle=True):
        self.addToQueue([Message,pickle])
        if pickle:
            print(f"sendt: {Message}")

    def checkServerLogic(self):
        while True:
            self.sendMessage("Test")
            time.sleep(2.5)

    def sendData(self):
        print("start sending thread")
        while Client.sending:
            for i in Client.sendingQueue:
                try:
                    if i[1]:
                        data = pickle.dumps(i[0])
                        self.sock.sendall(data)
                    else:
                        self.sock.sendall(i[0])
                    Client.sendingQueue.pop(0)
                except ConnectionResetError:
                    Client.sendingQueue.pop(0)
                    continue
        print("end sending thread")

    def listen(self):
        print("start listen thread")
        while Client.listening:
            data = self.testInput()
            if data:
                if data == "SERVER UPDATE":
                    Client.send = False
                    print("updating")
                    #sending file data
                    with open(self.filename,"rb") as f:
                        fileData = f.read(1024)
                        self.sendMessage("SERVERLOGIC")
                        self.sendMessage(fileData,False)
                        print("sent fileData")
                    Client.connected = False
                    self.sock.close()
                    self.__init__()
                else:
                    print(data)
        print("end listen thread")

    def requestUpdate(self):
        self.sendMessage("Update")
        print("update requested")



cl = Client()
threading.Thread(target=cl.sendData).start()
threading.Thread(target=cl.listen).start()
threading.Thread(target=cl.checkServerLogic).start()


time.sleep(5)
threading.Thread(target=cl.requestUpdate).start()
