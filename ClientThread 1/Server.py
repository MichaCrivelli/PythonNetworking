import threading
import socket
import pickle



class Server:
    def __init__(self):
        print("--- SERVER STARTED ---")
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addresse = '192.168.1.107',25000
        self.bound = False
        self.connections = []

        self.bindToAddress()

    def getCleanAddr(self,addr):
        ip = addr[0]
        port = addr[1]
        addr = f"{ip}:{port}"
        return addr

    def getAddressFromSock(self,sock):
        for i in self.connections:
            if i[0] == sock:
                return i[1]

    def getIndexBySock(self,sock):
        for i in self.connections:
            if i[0] == sock:
                return i

    def testSocket(self,sock):
        try:
            data = sock.recv(1024)
            return data
        except ConnectionResetError:
            print("connection expired")
            self.connections.remove(self.getIndexBySock(sock))
            return False

    def bindToAddress(self):
        self.sock.bind(self.addresse)
        print("Bound server to: ",self.getCleanAddr(self.addresse))
        self.bound = True

    def listening(self):
        print("Listening thread started")
        while True:
            if self.bound:
                #print("listening for connections")
                self.sock.listen()
                con,addr = self.sock.accept()
                self.connections.append((con,addr))
                print("connected to ",f"{addr[0]}:{addr[1]}")
        print("Listening thread ended")

    def printConnections(self):
        print("Data Thread started")
        while True:
            if self.bound:
                for i in self.connections:
                    sock = i[0]
                    data = self.testSocket(sock)
                    if data:
                        print("Got data from ",self.getCleanAddr(self.getAddressFromSock(sock)),"--> replying")
                        backData = b"GotYourData"
                        sock.sendall(backData)
        print("Data Thread started")


serv = Server()

threading.Thread(target=serv.listening).start()
threading.Thread(target=serv.printConnections).start()
