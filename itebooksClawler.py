# encoding=utf-8
# http://www.cnblogs.com/sirkevin/p/5783748.html
# http://www.allitebooks.com/
# http://www.allitebooks.com/page/1/ - http://www.allitebooks.com/page/709/
# 一页有10本, 总共 7006本 一本10M算  需要70G的空间
import traceback
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print "get books"
    pageUrls = ["http://www.allitebooks.com/page/{}/".format(str(i))for i in range(1,800)]
    pageUrls = ["http://www.allitebooks.com/page/{}/".format(str(i))for i in range(1,2)]
    print pageUrls
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    try:
        resp = requests.get(pageUrls.pop(), headers=headers)
        resp.encoding="utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        entry_titles = soup.findAll("h2",{"class":"entry-title"})
        for entry_title in entry_titles:
#             print entry_title
            link = entry_title.a.get('href')
            title = entry_title.a.string
            print link
            print title
    except:
        traceback.print_exc()