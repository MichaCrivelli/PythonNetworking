import pickle

# New Logic 1000


class simplelogic:

    def getCleanAddr(self,addr):
        ip = addr[0]
        port = addr[1]
        cleanAddr = f"{ip}:{port}"
        return cleanAddr

    def getAddressFromSock(self,sock):
        for i in self.connections:
            if i[0] == sock:
                return i[1]

    def closeServer(self):
        self.server[0].close()



    def main(self,data,connections,sock,server):
        self.server = server
        self.data = data
        self.connections = connections
        self.sock = sock
        self.addr = self.getAddressFromSock(self.sock)
        self.cleanAddr = self.getCleanAddr(self.addr)
        if data == "Test":
            reply = pickle.dumps(30)
            self.sock.sendall(reply)
