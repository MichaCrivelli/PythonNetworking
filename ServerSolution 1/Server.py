import socket, os
import threading
import pickle
import serverlogic
from serverlogic import SimpleLogic

class Server:

    connections = []
    queue = []
    queueLen = 0
    shutdown = False
    clientThread = False
    sendingThread = False
    dataThread = False


    def __init__(self):
        self.serverAddress = ("192.168.1.107",25000)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(self.serverAddress)
        print("bound to ",self.getCleanAddr(self.serverAddress))

    def getCleanAddr(self,addr):
        ip = addr[0]
        port = addr[1]
        return f"{ip}:{port}"

    def WriteServerLogic(self,fileData):
        path = "serverlogic2.py"
        f = open(path,"wb")
        f.write(fileData)
        print("wrote")

    def getAddrFromSock(self,sock):
        try:
            for i in Server.connections:
                if i[0] == sock:
                    return i[1]
        except:
            return "NaN"

    def SendingThread(self):
        print("---> SendingThread started")
        Server.sendingThread = True
        while not Server.shutdown:
            if len(Server.queue) > 0:
                index = Server.queue[0]
                if index[0] and index[1]:
                    sock = index[1]
                    print(index[0])
                    data = pickle.dumps(index[0])
                    sock.sendall(data)
                    Server.queue.remove(index)
                    Server.queueLen = len(Server.queue)
                    print("sent to: ",self.getAddrFromSock(sock))
                else:
                    print("could not send")
        Server.sendingThread = False
        print("---> SendingThread ended")

    def SendMessage(self,prefix,Message,sock):
        data = [prefix,Message]
        Server.queue.append([data,sock])

    def ClientThread(self):
        print("---> ClientThread started")
        Server.clientThread = True
        while not Server.shutdown:
            try:
                self.sock.listen()
                con,addr = self.sock.accept()
                Server.connections.append([con,addr])
                print("connected with: ",self.getCleanAddr(addr))
            except:
                continue

        Server.clientThread = False
        print("---> ClientThread stopped")

    def getData(self,con,pick = True):
        sock = con[0]
        addr = con[1]
        try:
            data = sock.recv(1024)
            if data:
                if pick:
                    data = pickle.loads(data)
                    return data
                else:
                    return data
        except ConnectionResetError:
            print(self.getCleanAddr(addr),": connection lost")
            Server.connections.remove(con)
            return False

    def Startshutdown(self):
        while True:
            if len(Server.queue) == 0:
                Server.shutdown = True
                self.sock.close()
                break

    def DataThread(self):
        print("---> DataThread started")
        Server.dataThread = True
        while not Server.shutdown:
            for i in Server.connections:
                data = self.getData(i)
                sock = i[0]
                if data:
                    if data[0] == "FileData":
                        print("getting Serverlogic")
                        fileData = data[1]
                        self.WriteServerLogic(fileData)
                        self.SendMessage("Message","Shutdown",sock)
                        self.Startshutdown()
                    else:
                        SimpleLogic.main(data,i)
        Server.dataThread = False
        print("---> DataThread stopped")

serv = Server()

ClientThread = threading.Thread(target=serv.ClientThread).start()
DataThread = threading.Thread(target=serv.DataThread).start()
sending = threading.Thread(target=serv.SendingThread).start()

while True:
    if Server.shutdown:
        if not Server.dataThread and not Server.sendingThread and not Server.clientThread:
            print("SHUTDOWN")
            os._exit(2)
