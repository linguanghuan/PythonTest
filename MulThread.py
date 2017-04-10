#http://www.cnblogs.com/fnng/p/3670789.html
#coding=utf-8

import threading
from threading import Timer, Thread
from time import sleep,ctime

mutex = threading.RLock()

def resource(item):
    print "CriticalResource, in use by", item

def lock(): #加锁
    mutex.acquire()

def unlock(): #解锁
    mutex.release()
    
def thread_test_lock(item):
    for i in range(20):
        if item==0:
            print "0000000000000000000000000000"
        else:
            print "11111111111111111111111111111"
        sleep(1)
        
    for i in range(20):
        lock()
        resource(item)
        sleep(1)
        unlock()
        
def thread_test_join(item):
    if item == 0:
        print "0000000000000000000000000000", ctime()
        sleep(5)
        print "0000000000000000000000000000", ctime()
    else:
        print "11111111111111111111111111111", ctime()
        sleep(3)
        print "11111111111111111111111111111", ctime()
    
if __name__ == "__main__":
    thread_count = 2
    threads = []
    for item in xrange(thread_count):
        t=threading.Thread(target=thread_test_join, args=(item,))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print "main"
    while True:
        print "main loop"
        sleep(10)
    