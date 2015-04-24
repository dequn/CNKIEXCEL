#coding=utf-8
from YearBook import *
import socket
import myutils
from pyquery import PyQuery
import threading
import random,time


reload(sys)

sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(120)

class Test(threading.Thread):
    def __init__(self,root,url):
        threading.Thread.__init__(self)
        self.root = root
        self.url = url
    def run(self): 
        print '%s,%s' %(self.root,self.url)
        time.sleep(random.randint(0,10))
        print '%s is over' %(self.root)
        
class NianJian(threading.Thread):
    def __init__(self,root,url):
        self.root = root
        if not os.path.exists(self.root):
            try:
                os.mkdir(self.root)
            except Exception:
                print '%s not exists or error,please check it.' % (self.root)
                sys.exit()
        threading.Thread.__init__(self)
        self.url = url
        self.root = root
        self.req_header ={"Accept":ur"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":ur"gzip, deflate, sdch",
    "Accept-Language":ur"en,zh-CN;q=0.8,zh;q=0.6",
    "Connection":ur"keep-alive",
    "Host":ur"tongji.cnki.net",
    "User-Agent":ur"Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"
    }
        self.threads = []
    def run(self):
        self.get_year_of_nianjian()
    def get_year_of_nianjian(self):
        req = urllib2.Request(self.url,None,self.req_header)
        response = urllib2.urlopen(req)
        rawdata= myutils.ungzip(response)
        year_num = len(PyQuery(rawdata.decode('utf-8'))(".list_h li a"))
        i = 0 
        while i < year_num:
            j = 0
            while j < 5 and i < year_num:
                li = PyQuery(PyQuery(rawdata.decode('utf-8'))(".list_h li a")[i])
                folder = myutils.filenameCheck(li.text())
                folder = os.path.join(self.root,folder)
                try:
                    os.mkdir(folder)
                except Exception,e:
                    print "%s created error" %(folder)
                    i = i + 1
                    j = j + 1
                else:
                    href = "http://tongji.cnki.net/kns55/Navi/" + li.attr("href")
                    i = i + 1
                    j = j + 1
                    self.threads.append(YearPage(os.path.join(self.root,li.text()),href))
            for t in self.threads:
                if not t.isAlive():
                    t.start()
            t.join()
            self.threads = []

