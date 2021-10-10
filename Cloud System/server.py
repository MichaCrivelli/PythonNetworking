import socket
import ServerLogic
import ast
import pickle
from multiprocessing import Process
import time

print("--- SERVER STARTED ---")
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

connections = []

def readSaveFile():
    with open("save.txt","r") as f:
        save = f.read()
        save = ast.literal_eval(save)
        addr = save["Server"]["addr"]
        return addr

Address = readSaveFile()

def main():
    global connections
    logic = True

    sock.bind(Address)
    print("bound server to ", Address)

    while True:
        print("listening...")
        sock.listen()

        con,addr = sock.accept()
        print(addr," connected\n")
        connections.append(con)
        #connections[f"{addr[0]}:{addr[1]}"] = con
        print(connections)

def HearConnections():
    global connections
    while True:
        print(connections)
        for i in connections:
            print(i)

            '''
            clSock = connections[i]

            data = clSock.recv(1024)
            if data:
                print("--"*3+"got Data")
                if data == "restart":
                    print("RESTART")
                ServerLogic.Main()'''
        time.sleep(1)

if __name__=="__main__":
    serverHear = Process(target=HearConnections)
    serverListen = Process(target=main)
    serverHear.start()
    serverListen.start()
