#https://zhuanlan.zhihu.com/p/24835141
#coding=utf-8

"""
Created on Sat Aug 27 21:18:12 2016
 
@author: 独处
"""
 
import requests
from bs4 import BeautifulSoup
import threading
import os
import traceback
import chardet

# http://wangye.org/blog/archives/629/
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

basePath = "F:/meitulu/"
threadLimit = 30
 
os.chdir(basePath)
 
urlPool = ["http://www.meitulu.com/item/{}.html".format(str(i))for i in range(5000,6000)]
numMutex = threading.Lock()
#以g开头，意味着这是一个全局变量
g_threadNum = 0
 
def downloadImg(url):
    dirname = url.split("/")[-1].split(".")[0]
    if os.path.exists(dirname):
        print("dir already exist: " + dirname)
        return
    print "deal: " + dirname
    ordinal = 1
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}
    linkPool = []
    try:
        resp = requests.get(url,headers=headers)
        # 
        resp.encoding="utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        title = soup.select("head > title")[0].string
#         title2 = title.decode("gbk").encode("utf-8");
#         print "title: " + title + " " + title2
        dirname = dirname + "_" + title
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        content = title
        try:
            info = soup.select("body > div.width > div.c_l")[0].text
#             print info
            content = content + "\n" + info
        except:
            traceback.print_exc()
        try:
            desc = soup.select("body > div.width > p")[0].text
#             print desc
            content = content  + "\n" + desc
        except:
            traceback.print_exc()
            pass
        try:
            tags = soup.select("#fenxiang > div.fenxiang_l")[0].text
            tags = tags.replace("\n", ",")
            content = content  + "\n" + tags
        except:
            traceback.print_exc()
            
        print content
        file = open(dirname +"/" + title + ".txt","w")
        file.write(content)
        file.close()
    except:
        traceback.print_exc()
    
    while True:
        try:
            links = soup.select("body > div.content > center > img")
            for urlLink in links:
                link = urlLink.get("src")
                linkPool.append(link)
            nextPageUrl = soup.findAll("a",{"class":"a1"})[1].get("href")
            if nextPageUrl == url :
                break
            else:
                url = nextPageUrl
                resp = requests.get(url,headers=headers)
                # 
                resp.encoding="utf-8"
                soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            #这里没有用锁，好吧，也就这样了，应该不会出现什么问题吧，最多是不好看而已
            print("Connection Error, or BeautifulSoup going Wrong, forget it:",url)
            break
             
    for link in linkPool:
        try:
            print "download image:" + link
            timestamp = link[-21:-4]
            print "timestamp:" + timestamp
            content = requests.get(link,headers = headers)
            title = timestamp + ".jpg"
            #文件就保存在工作目录了
            file = open(dirname +"/" + title,"wb")
            file.write(content._content)
            file.close()
            ordinal += 1
        except Exception :
            print("Couldn't Parse!",link)
            traceback.print_exc()
            break
 
 
class MyThread(threading.Thread):
    def __init__(self,url):
        self.url = url
        threading.Thread.__init__(self)
     
    def run(self):
        downloadImg(self.url)
        numMutex.acquire()
        global g_threadNum
        g_threadNum -= 1
        numMutex.release()
 
 
while urlPool != []:
    #如果线程比较少，就
    if g_threadNum < threadLimit:
        newUrl = urlPool.pop()
        g_threadNum += 1
        newThread = MyThread(newUrl)
        newThread.start()