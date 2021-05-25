import pickle

class SimpleLogic:

    def main(data,con):
        data = data
        sock = con[0]
        if data[0] == "Message":
            print(data[1])
            reply = pickle.dumps(["Message",data[1]])
            sock.sendall(reply)
