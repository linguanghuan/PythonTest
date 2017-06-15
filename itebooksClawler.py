# encoding=utf-8
# http://www.cnblogs.com/sirkevin/p/5783748.html
# http://www.allitebooks.com/
# http://www.allitebooks.com/page/1/ - http://www.allitebooks.com/page/709/
# 一页有10本, 总共 7006本 一本10M算  需要70G的空间
#pip install requests
#pip install bs4
#pip install lxml
#pip install bs4
#pip install threadpool

import traceback
import requests
from bs4 import BeautifulSoup
import threadpool
import sys
import os
import datetime
import threading
import shutil
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')

g_lock = threading.Lock()

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
recordFile = "all_files_"+today+".txt"
newPath = "E:/book2/"
oldPath = "E:/allitebooks"
failedFile = "E:\\book2\\perm_error.txt"
manualPath = "E:/allitebooks_manual"
os.chdir(newPath)
recordfd = open(recordFile, "a") 

pageUrls = ["http://www.allitebooks.com/page/{}/".format(str(i+1))for i in range(715, -1, -1)]
exist = {}
linkPool = []

def loadExists():
    os.chdir(oldPath)
    subdirs = os.listdir(os.getcwd());
    for subdir in subdirs:
        exist[subdir] = "1"
    print "exist len:", len(exist)
    sleep(3)    
    try:
        filefd = open(failedFile, "r")
        for line in filefd:
            exist[line.strip()] = "1" # 需要trim掉回车
        filefd.close()    
    except:
        traceback.print_exc()
        sys.exit()
    print "exist len:", len(exist)
    sleep(3)
        
def checkExist(key):
    try:
        if exist[key]=="1":
            return True
        return False
    except:
        return False

def mov(src, dst):
    shutil.move(src, dst)
        
def getPdfBook(link):
    try:
        print "=======================begin to get book", link
        dirname = link.split("/")[3]
        print "dirname", dirname
        if checkExist(dirname)==True:
            print "skip exist job", dirname
            return
        
        if not os.path.isdir(dirname):
            try:
                os.mkdir(dirname)
            except:
                traceback.print_exc()
                return
        success_mark = os.path.join(dirname, "success_mark.txt")   
        if os.path.exists(success_mark):
            print "skip success job:", dirname
            return
        
        resp = requests.get(link, headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        try:
            detail = soup.find("div",{"class":"book-detail"}).get_text()
            print "detail", detail
            desc = soup.find("div",{"class":"entry-content"}).get_text()
            print "desc", desc
            
        except:
            traceback.print_exc()
        try:
            downloadLink =  soup.find("span",{"class":"download-links"}).a.get('href')
            print "download", downloadLink
            filename = downloadLink.split("/")[-1]
        except:
            traceback.print_exc()
            return
        
        fullFileName = dirname+"/"+filename
        manualFile =  os.path.join(manualPath, filename)
        if os.path.exists(fullFileName):
            print "file already exist:",  fullFileName
            return
        elif os.path.exists(manualFile):
            print "move from manual path"
            mov(manualFile, fullFileName)
            return
        try:
            descFile = dirname + "/" + dirname + ".txt"
            filefd = open(descFile,"w")
            filefd.write(detail)
            filefd.write(desc)
        except:
            traceback.print_exc()
        finally:
            filefd.close()
            
        content = requests.get(downloadLink, headers = headers)
        try:
            filefd = open(fullFileName,"wb")
            filefd.write(content._content)
            filefd.close()
        except:
            traceback.print_exc()
        finally:
            filefd.close()
    except:
        traceback.print_exc()

def test():
    print range(708, -1, -1)
    return
    teststr = "http://www.allitebooks.com/build-mobile-apps-with-ionic-2-and-firebase/"
    print teststr.split("/")[3]
    str2 = "http://file.allitebooks.com/20170505/Build Mobile Apps with Ionic 2 and Firebase.pdf"
    print str2.split("/")[-1]

    
def getBooks(pageUrl):  
    try:
        print "deal", pageUrl
        resp = requests.get(pageUrl, headers=headers, timeout=30)
        resp.encoding="utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        entry_titles = soup.findAll("h2",{"class":"entry-title"})
        for entry_title in entry_titles:
#             print entry_title
            link = entry_title.a.get('href')
#             title = entry_title.a.string
            print "get", link
#             print title
            linkPool.append(link)
            g_lock.acquire()
            recordfd.write(link + '\n')
            g_lock.release()
        recordfd.flush()
        return True
    except:
        traceback.print_exc() 
        pageUrls.append(pageUrl)
        return False
                 
if __name__ == "__main__":
#     test()
    loadExists()
    if checkExist("a-tour-of-c")==True:
        print "111111111"
#     sys.exit()
    print "allitebooks clawler"
    
    os.chdir("E:/book2/")
    if os.path.exists(recordFile) and os.path.getsize(recordFile) > 10:
        try:
            filefd = open(recordFile, "r")
            for line in filefd:
                linkPool.append(line)
        except:
            traceback.print_exc()
            sys.exit()
    else:
        try:
            filefd = open(recordFile, "w")
            pool = threadpool.ThreadPool(40)
            threadRequests = threadpool.makeRequests(getBooks, pageUrls)
            [pool.putRequest(req) for req in threadRequests]
            pool.wait()
        except:
            traceback.print_exc()
        finally:
            file.close()
            
    print "link pool size:", len(linkPool)
    sleep(3)
#     sys.exit()

    os.chdir(newPath)            
    pool = threadpool.ThreadPool(40)
    threadRequests = threadpool.makeRequests(getPdfBook, linkPool)
    [pool.putRequest(req) for req in threadRequests]
    pool.wait()
    print "finishied"
        
        