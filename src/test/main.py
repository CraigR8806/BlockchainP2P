import threading
from time import sleep
from src.p2p.dataservice import DataService

global r1, r2, r3
r1 = True
r2 = True
r3 = True

def do_the_thing1(ds):
    while r1:
        ds.modify("i", lambda v:v.update({"a": v["a"] + 1}), asyync=True)

def do_the_thing2(ds):
    while r2:
        ds.modify("i", lambda v:v.update({"b": v["b"] + 1}), asyync=False)

def do_the_thing3(ds):
    while r3:
        ds.modify("i", lambda v:v.update({"c": v["c"] + 1}), asyync=False)





def testThreads():

    i={"a":0,"b":0}
    i.update({"c":0})
    print("c" not in i)

    print((lambda :len(i)<=0)())


    print("--------------------------------------------------------------------------------")


    ds = DataService()

    ds.start_service()
    ds.add("i", i)

    t1 = threading.Thread(target=do_the_thing1, args=[ds])
    t2 = threading.Thread(target=do_the_thing2, args=[ds])
    t3 = threading.Thread(target=do_the_thing3, args=[ds])
    t1.start()
    print("here")
    t2.start()
    print("here2")
    t3.start()
    print("here3")

    sleep(.0001)

    print("here4")

    global r1, r2, r3
    r1 = False
    r2 = False
    r3 = False

    t1.join()
    t2.join()
    t3.join()


    o = ds.deep_copy("i")
    print(str(o))
    ds.stop_service()

    print(ds.get_highest_queue_count())


def main():
    print(list(range(0,1)))
    

if __name__ == '__main__':
    main()
