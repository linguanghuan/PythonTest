#http://www.cnblogs.com/fnng/p/3670789.html
#coding=utf-8

import threading
from threading import Timer, Thread
from time import sleep,ctime
from random import randint
#pip install threadpool
import threadpool
from threadpool import ThreadPool

mutex = threading.RLock()

def resource(item):
    print "CriticalResource, in use by", item

def lock(): #加锁
    mutex.acquire()

def unlock(): #解锁
    mutex.release()
    
def thread_func_lock(item):
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
        
def thread_func_join(item):
    if item == 0:
        print "0000000000000000000000000000", ctime()
        sleep(5)
        print "0000000000000000000000000000", ctime()
    else:
        print "11111111111111111111111111111", ctime()
        sleep(3)
        print "11111111111111111111111111111", ctime()

def thread_sub():
    sleepSeconds= randint(1,5)
    print "subbbbbbbbbbbbbbbb", sleepSeconds , ctime()
    sleep(sleepSeconds)
    print "subbbbbbbbbbbbbbbb", sleepSeconds , ctime()
    
def thread_with_thread(item):
    if item == 0:
        print "0000000000000000000000000000", ctime()
        sleep(5)
        print "0000000000000000000000000000", ctime()
    else:
        print "11111111111111111111111111111", ctime()
        sleep(3)
        print "11111111111111111111111111111", ctime()
        
def test_thread_join():
    thread_count = 3
    threads = []
    for item in xrange(thread_count):
        t=threading.Thread(target=thread_func_join, args=(item,))
        threads.append(t)
        
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    print "main"
    while True:
        print "main loop"
        sleep(10)

def hello(str): 
    sleep(2) 
    return str 
 
def print_result(request, result): 
    print "the result is %s %r" % (request.requestID, result) 
                    
def test_thread_pool():
    #http://dgfpeak.blog.51cto.com/195468/861994
    #http://jishublog.iteye.com/blog/1898971
    print "test thread_pool"
    data = [randint(1,10) for i in range(20)] 
    pool = threadpool.ThreadPool(5) 
    requests = threadpool.makeRequests(hello, data, print_result) 
    [pool.putRequest(req) for req in requests] 
    pool.wait() 
    
if __name__ == "__main__":
#     test_thread_join()
    test_thread_pool()
    test_thread_pool()
    