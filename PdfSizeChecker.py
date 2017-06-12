import traceback
import os
import re
import shutil

def getSizeFromTxt(path):
    try:
        fp = open(path)
        all_text = fp.read()
#         print all_text
        pattern = re.compile("File size: (.+) MB")
        size = re.findall(pattern, all_text)[0]
        print path, " size:", float(size)*1024*1024
        return float(size)*1024*1024
    except:
        traceback.print_exc()
        print "except", path
        return 0
    finally:
        fp.close()
    
def mov(src, dst):
    shutil.move(src, dst)
    
def sizecheck(dir):    
    try:
        error = 0;
        success = 0;
        unknow = 0;
        total = 0;
        os.chdir(dir);
        subdirs = os.listdir(os.getcwd());
        print len(subdirs)
        for subdir in subdirs:
            print "============",subdir,"============"
            files = os.listdir(subdir)
            filesize = 0.0
            size_from_txt = 0.0
            total = total + 1
            for file in files:
                path = os.path.join(subdir,file)    
                if file.endswith("pdf"):
                    filesize = os.path.getsize(path)
                    print path, " size ", filesize
                if file.startswith(subdir) and file.endswith("txt"):
#                     print "txt desc file", path
                    size_from_txt = getSizeFromTxt(path)
            if size_from_txt==0:
                print "========unknow", subdir
                unknow = unknow + 1
                mov(subdir, "E:\\part\\unknow\\")
                continue
            
            radio = (filesize / size_from_txt)        
            print "pdf:", filesize, ",txt:", size_from_txt, ",radio", radio
            if filesize > 1 and size_from_txt > 1 and radio > 0.97:
                print "=======success:", subdir
                success = success + 1
                mov(subdir, "E:\\part\\succ\\")
            else:
                print "=======error: ", subdir
                error = error + 1
                mov(subdir, "E:\\part\\fail\\") 
        
        print "total:", total, ", success:", success, ", error:", error, ",unknow:", unknow
    except:
        traceback.print_exc()

if __name__=="__main__":
    sizecheck('E:\\allitebooks')