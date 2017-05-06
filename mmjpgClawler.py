#https://zhuanlan.zhihu.com/p/26395979
#coding=utf-8

import requests
# pip install lxml
from lxml import html
import os
import traceback
import threadpool

def get_a_mm(num):
    dir = "C:/Users/test/Desktop/mmjpg/"
    num = num + 1
    url = "http://www.mmjpg.com/mm/"+str(num);
    print url
    try:
        content = requests.get(url).content
    #     print response
        selector = html.fromstring(content)
        title = selector.xpath("//h2/text()")[0]
        print title
        save_dir = dir +str(num) + "_" + title + "/"
        if os.path.exists(save_dir) == False:
            os.makedirs(save_dir)
        else:
            print save_dir + " already exist"
            return
            
        keyword_list = selector.xpath("/html/head/meta[2]/@content")
        keyword = "".join(keyword_list)
        print keyword
        image_count = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
        print image_count
        image_num = int(image_count);
        for subnum in range(image_num):
            try:
                sub_url = "http://www.mmjpg.com/mm/" + str(num) + "/" + str(subnum + 1);
                print sub_url
                subContent = requests.get(sub_url).content
                selector = html.fromstring(subContent)
                image = selector.xpath("//*[@id='content']/a/img/@src")[0]
                print image     
                filename = save_dir + str(num) + "_" + str(subnum+1) + ".jpg"
                print filename
                with open(filename, 'wb') as f:
                    f.write(requests.get(image).content)
            except:
                traceback.print_exc()
    except:
        traceback.print_exc()
    
if __name__ == "__main__":
#     996
#     dir = "C:/Users/test/Desktop/mmjpg/";
    mms = range(961)
    pool = threadpool.ThreadPool(30)
    threadRequests = threadpool.makeRequests(get_a_mm, mms)
    [pool.putRequest(req) for req in threadRequests]
    pool.wait()
#     for num in range(961):
#         url = "http://www.mmjpg.com/mm/" + str(num + 1)
#         print url
#         try:
#             
#             get_a_mm(dir, num+1)
#         except:
#             traceback.print_exc()