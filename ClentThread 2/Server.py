import threading
import socket
import pickle
import serverlogic
from serverlogic import simplelogic
import os
import subprocess

class Server:

    shutdown = False

    def __init__(self):
        print("--- SERVER STARTED ---")
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addresse = '192.168.1.107',20001
        self.bound = False
        self.connections = []
        self.simplelogic = simplelogic()

        self.bindToAddress()

    def closeServer(self):
        self.sock.close()
        print("closed server")

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

    def testSocket(self,sock,pick = True):
        try:
            data = sock.recv(1024)
            if data:
                if pick:
                    data = pickle.loads(data)
                    return data
                else:
                    return data
            else:
                return False
        except ConnectionResetError:
            print("connection expired")
            self.connections.remove(self.getIndexBySock(sock))
            return False

    def updateServer(self,sock,data):
        if data == "Update":
            reply = pickle.dumps("SERVER UPDATE")
            sock.sendall(reply)
        if data == "SERVERLOGIC":
            print("initializing update")
            data = sock.recv(1024)
            with open("serverlogic2.py","wb") as f:
                print(data)
                f.write(data)
            Server.shutdown = True

    def bindToAddress(self):
        self.sock.bind(self.addresse)
        print("Bound server to: ",self.getCleanAddr(self.addresse))
        self.bound = True

    def listening(self):
        print("Listening thread started")
        while not Server.shutdown:
            if self.bound:
                #print("listening for connections")
                self.sock.listen()
                con,addr = self.sock.accept()
                self.connections.append((con,addr))
                print("connected to ",f"{addr[0]}:{addr[1]}")
        print("Listening thread ended")

    def dataThread(self):
        print("Data Thread started")
        while not Server.shutdown:
            if self.bound:
                for i in self.connections:
                    sock = i[0]
                    data = self.testSocket(sock)
                    if data:
                        print(data)
                        self.updateServer(sock,data)
                        self.simplelogic.main(data,self.connections,sock,self.sock)
        print("Data Thread stopped")

serv = Server()

threading.Thread(target=serv.listening).start()
threading.Thread(target=serv.dataThread).start()

while True:
    if Server.shutdown:
        print("SHUTDOWN")
        os._exit(2)
        subprocess.call([r"start.bat"])
