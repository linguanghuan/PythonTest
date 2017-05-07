# encoding=utf-8
# http://www.cnblogs.com/sirkevin/p/5783748.html
# http://www.allitebooks.com/
# http://www.allitebooks.com/page/1/ - http://www.allitebooks.com/page/709/
# 一页有10本, 总共 7006本 一本10M算  需要70G的空间

import traceback
import requests
from bs4 import BeautifulSoup
import threadpool
import sys
import os
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

linkPool = []
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
basePath = "F:/allitebooks"
os.chdir(basePath)

def get_a_book(link):
    try:
        print "=======================begin to get book", link
        dirname = link.split("/")[3]
        print "dirname", dirname
        if not os.path.isdir(dirname):
            try:
                os.mkdir(dirname)
            except:
                traceback.print_exc()
                return
            
        if os.path.exists(os.path.join(dirname, "success_mark.txt")):
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
        if os.path.exists(fullFileName):
            print "file already exist:",  fullFileName
            return
        try:
            descFile = dirname + "/" + dirname + ".txt"
            file = open(descFile,"w")
            file.write(detail)
            file.write(desc)
        except:
            traceback.print_exc()
        finally:
            file.close()
            
        content = requests.get(downloadLink, headers = headers)
        try:
            file = open(fullFileName,"wb")
            file.write(content._content)
            file.close()
        except:
            traceback.print_exc()
        finally:
            file.close()
    except:
        traceback.print_exc()

def test():
    print range(708, -1, -1)
    return
    str = "http://www.allitebooks.com/build-mobile-apps-with-ionic-2-and-firebase/"
    print str.split("/")[3]
    str2 = "http://file.allitebooks.com/20170505/Build Mobile Apps with Ionic 2 and Firebase.pdf"
    print str2.split("/")[-1]

    
if __name__ == "__main__":
#     test()
#     sys.exit()
    print "allitebooks clawler"
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    recordFile = "all_files_"+today+".txt" 
    if os.path.exists(recordFile):
        try:
            file = open(recordFile, "r")
            for line in file:
                linkPool.append(line)
        except:
            traceback.print_exc()
            sys.exit()
    else:
        pageUrls = ["http://www.allitebooks.com/page/{}/".format(str(i+1))for i in range(299, -1, -1)]
    #     pageUrls = ["http://www.allitebooks.com/page/{}/".format(str(i))for i in range(1,2)]

        try:
            file = open(recordFile, "w")
            while len(pageUrls) > 0:
                try:
                    pageUrl = pageUrls.pop()
                    print "deal", pageUrl
                    resp = requests.get(pageUrl, headers=headers)
                    resp.encoding="utf-8"
                    soup = BeautifulSoup(resp.text, "lxml")
                    entry_titles = soup.findAll("h2",{"class":"entry-title"})
                    for entry_title in entry_titles:
            #             print entry_title
                        link = entry_title.a.get('href')
                        title = entry_title.a.string
                        print "get", link
            #             print title
                        linkPool.append(link)
                        file.write(link + '\n')
                    file.flush()
                except:
                    traceback.print_exc()
        except:
            traceback.print_exc()
        finally:
            file.close()
                
    pool = threadpool.ThreadPool(40)
    threadRequests = threadpool.makeRequests(get_a_book, linkPool)
    [pool.putRequest(req) for req in threadRequests]
    pool.wait()
    print "finishied"
        
        