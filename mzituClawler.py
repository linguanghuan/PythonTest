#encoding:utf-8
#http://www.mzitu.com/

import os
import traceback
import requests;
from bs4 import BeautifulSoup
import re
from re import match
from Queue import Queue
import sys
import time

import threading
from threading import Timer, Thread
import threadpool
from threadpool import ThreadPool

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
saveDir = "C:/Users/test/Desktop/mzitu/"
if os.path.exists(saveDir)==False:
    os.mkdir(saveDir);
os.chdir(saveDir)

mmPool = Queue()
pageUrls=Queue()
threadResouces = threading.Semaphore(100)

def SavePic(url):
    try:
        id = url.split("/")[-1]
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        picCount = soup.select("body > div.main > div.content > div.pagenavi > a > span")[4].text
        title = soup.select("body > div.main > div.content > h2")[0].text
        desc="title:" + title + "\n"
        category=soup.select("body > div.main > div.content > div.main-meta > span > a")[0].text
        desc += "category:" + category + "\n"
        tags = soup.select("body > div.main > div.content > div.main-tags > a")
        tagsStr =",".join(tag.text for tag in tags)
        desc += "tags:" + tagsStr + "\n"
        desc += "count:" + picCount + "\n"
        timestamp = soup.select("body > div.main > div.content > div.main-meta > span")[1].text
        desc += timestamp + "\n"
        print desc
        dir = id + "_" + title + "["+picCount+"]"
        if os.path.exists(dir):
            print("dir already exist: " + dir)
            threadResouces.release()
            return
        os.mkdir(dir);
        try:
            file = open(dir +"/" + "desc.txt","w")
            file.write(desc)
        except:
            traceback.print_exc()
        finally:
            file.close()
            
#         return
    
        for i in range(int(picCount)):
            try:
                picUrl = "http://www.mzitu.com/" + id + "/" + str(i+1)
                print picUrl
                resp = requests.get(picUrl, headers=headers)
                soup = BeautifulSoup(resp.text, "lxml")
                img = soup.select("body > div.main > div.content > div.main-image > p > a > img")[0].get("src")
                print img
                content = requests.get(img,headers = headers)
                filename = img.split("/")[-1]
                file = open(dir +"/" + filename,"wb")
                file.write(content._content)
                file.close()
            except:
                traceback.print_exc()
    except:
        traceback.print_exc()
    threadResouces.release()
        
def mulThreadDeal():
    while True:
        if mmPool.qsize() > 0:
            threadResouces.acquire()
            url = mmPool.get()
            t=threading.Thread(target=SavePic, args=(url,))
            t.setDaemon(True)
            t.start()
        else:
            time.sleep(1)
     
if __name__=="__main__":
#     SavePic("http://www.mzitu.com/90792")
#     sys.exit()

    pageUrls.put("http://www.mzitu.com/")
    
    visitedPage = {}
    
    threadCount=3
    t=threading.Thread(target=mulThreadDeal, args=())
    t.setDaemon(True)
    t.start()
    
    pattern = re.compile(r'^http://www.mzitu.com/\d{1,9}$')
    pattern2 = re.compile(r'^http://www.mzitu.com/.+$')
    while pageUrls.empty()==False:
        url = pageUrls.get()
        if visitedPage.has_key(url):
            print "is visited", url
            continue
        try:
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, "lxml")
            for a in soup.findAll('a', href=True):
                link = a['href']
                if pattern.match(link):
                    print "mm link:", link
                    mmPool.put(link)
                    if mmPool.qsize() > 1000:
                        print "mmPool", mmPool.qsize(), "sleep 5s"
                        time.sleep(5)
                elif pattern2.match(link):
                    print "page link:", link
                    pageUrls.put(link)
                    if pageUrls.qsize()%100 == 0:
                        print "===============pageUrls len:", pageUrls.qsize()
                else:
                    print "ignore:" , link
        except:
            traceback.print_exc()
        finally:
            visitedPage[url]=True
            if len(visitedPage) %100 == 0:
                print "===============visitedPage len:", len(visitedPage)
        
        
    