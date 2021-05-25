from multiprocessing import Process, current_process

def sqare():
    num = 0
    while num < 100:
        print("sqare")

        num += 1

def dupli():
    num = 0
    while num < 100:
        print("dupli")
        num += 1

if __name__ == "__main__":

    processes = []
    proc = Process(target=sqare)
    proc1 = Process(target=dupli)
    proc.start()
    proc1.start()
