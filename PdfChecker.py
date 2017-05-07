# encoding:utf-8
# ref: http://hao.jobbole.com/pdfminer/
# ref: http://www.bkjia.com/Pythonjc/1073800.html

import os
import traceback
# pip install pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from Queue import Queue
from Queue import Empty
import threadpool
import shutil
import sys

all_pdf_files = []
failed_files = Queue()
succed_files = Queue()
skip_path = Queue()

fail_dir ="F:\\failedbooks\\"
if os.path.exists(fail_dir)==False:
    os.makedirs(fail_dir)
    
def fail_test():
    try:
        os.chdir(r'F:\allitebooks\oracle-nosql-database')
        fp = open('Oracle NoSQL Database.pdf', 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
    except:
        traceback.print_exc()
    finally:
        fp.close()

def succ_test():
    try:
        os.chdir(r'F:\allitebooks\making-games')
        fp = open('Making Games.pdf', 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        print "extractable:",document.is_extractable, ",modifiable:",document.is_modifiable,", printable:", document.is_printable
        outlines = document.get_outlines()
        print outlines
    except:
        traceback.print_exc()
    finally:
        parser.close()
        fp.close()

def get_all_files(dir):
    try:
        g = os.walk(dir)
        for path, subdir, filelist in g:
#             print '----------------------------'
#             print "path:", path, "subdir:", subdir
            if "success_mark.txt" in filelist:
                print "skip success dir:", path
                skip_path.put(path)
                continue
            for filename in filelist:
                file = os.path.join(path, filename)
                if file.endswith("pdf"):
                    print "found pdf", file
                    all_pdf_files.append(file)
        print "**********************skiped path count", skip_path.qsize()
    except:
        traceback.print_exc()

def check_pdf(file):
    failed = False
    print "check_pdf:", file
    try:
        fp = open(file, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        print "extractable:",document.is_extractable, ",modifiable:",document.is_modifiable,", printable:", document.is_printable
        succed_files.put(file)
        succed_path = os.path.split(file)[0]
        succed_mark_file = os.path.join(succed_path, "success_mark.txt")
        f = open(succed_mark_file, "w")
        f.close()
        print "succed mark file generated:", succed_mark_file
    except:
        traceback.print_exc()
        failed_files.put(file)
        failed = True
#         print "move fail file to dir", fail_dir, ",", file
#         shutil.move(file, fail_dir)  # 必须先关闭文件才能移动，不然报错  os.unlink(src) WindowsError: [Error 32]  http://jining2593.blog.163.com/blog/static/2770148420101024114428257/
    finally:
        parser.close()
        fp.close()
        if failed == True:
            print "move fail file to dir", fail_dir, ",", file
            shutil.move(file, fail_dir)
        print "all:", len(all_pdf_files), ",succed:", succed_files.qsize(), ",failed:", failed_files.qsize()

def remove_test(file):
#     F:\\failedbooks\\Mastering FreeSWITCH.pdf  必须2个斜杠，不然会被当成转义子字符
    os.remove(file)

def unlink_test(file):
    os.unlink(file)
               
if __name__ == "__main__":
#     fail_test()
#     succ_test()
#     remove_test("F:\\failedbooks\\Mastering FreeSWITCH.pdf")
#     unlink_test("F:\\failedbooks\\3D Game Environments.pdf")
#     sys.exit()

    get_all_files('F:\\allitebooks')

    print "get pdf file count:", len(all_pdf_files)
    pool = threadpool.ThreadPool(50)
    threadRequests = threadpool.makeRequests(check_pdf, all_pdf_files)
    [pool.putRequest(req) for req in threadRequests]
    pool.wait()    
    print "failed:", failed_files.qsize()
    print "succed:", succed_files.qsize()
    print "filelist:"
    while True:
        try:
            fail = failed_files.get()
            print fail
        except Empty:
            break  

  
    