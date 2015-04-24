#coding=utf-8

import sys,os,copy,shutil
from pyquery import PyQuery
from urllib2 import Request
from cookielib import CookieJar
import urllib2,urllib,cookielib
import webtest2,myutils
import socket

socket.setdefaulttimeout(60)
reload(sys)
sys.setdefaultencoding('utf-8')
    
class YearPage():
    def __init__(self,root):
        pass
        self.req_header ={"Accept":ur"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":ur"gzip, deflate, sdch",
    "Accept-Language":ur"en,zh-CN;q=0.8,zh;q=0.6",
    "Cache-Control":ur"max-age=0",
    "Connection":ur"keep-alive",
    "Host":ur"tongji.cnki.net"}
        myutils.get_cookieJar()
        self.cookieJar = myutils.g_cookieJar
        self.root = root
    def parse_yearbook_page(self,url):
        req = urllib2.Request(url,None,self.req_header)
        try:
            response = urllib2.urlopen(req)
        except Exception,e:
            f = open(os.path.join(root,"year_error.txt"),'a')
            f.write('%s---%s\n' % (self.root,url))
            f.close()
        else:
            rawdata= myutils.ungzip(response)
    #         print rawdata
            pquery = PyQuery(rawdata.decode('utf-8'))
            for li in pquery(".TreeList li"):
    
                self.pfolder = PyQuery(li)("a").text()
                if os.path.exists(os.path.join(self.root,self.pfolder)):
                    self.pfolder = self.pfolder + "_2"
                os.mkdir(os.path.join(self.root,self.pfolder))
        
                strParam = PyQuery(li)("a").attr('onclick')
                aParam = strParam.split('(')[1].strip(')').split(',')
                param = {}
                param["id"] = aParam[0].strip().strip("'")
                param["code"] = aParam[1].strip().strip("'")+ "?"
                param["type"] = aParam[2].strip().strip("'")
                param["fileid"] = aParam[3].strip().strip("'")
                self.get_child_catalog(param)
            self.deal_error()
    def get_child_catalog(self,param):

        url = "http://tongji.cnki.net/kns55/Navi/GetChildCatalog.aspx"
        
        req = urllib2.Request(url,urllib.urlencode(param),self.req_header)
#         print req.get_full_url()
        try:
            response = urllib2.urlopen(req)
        except Exception,e:
            f = open(os.path.join(self.root,"get_child_error.txt"),'a')
            f.write('%s---%s---%s\n' % (self.root , self.pfolder,urllib.urlencode(param)))
            f.close()
        else:
            rawdata = myutils.ungzip(response)
    #         print rawdata
            pas = PyQuery(rawdata.decode('utf-8'))(".dhmltable-biaotou-rightspan")("a")
            for a in pas:
                click_data = PyQuery(a).attr("onclick")
                datas = click_data.split(",")

                param["sf"] = datas[0].split('(')[1].strip("'")
                param["page"] = datas[1].strip().strip("'").strip()
                param["name"] = datas[2].split(')')[0].strip().strip("'").strip()
                param["type"] = '3'
                if param.has_key("fileid"):
                    del param["fileid"]
                self.pages(param)
            
            
    def pages(self,param):
        url = "http://tongji.cnki.net/kns55/Navi/Page.aspx"
        
        req = urllib2.Request(url,urllib.urlencode(param),self.req_header)
#         print req.get_full_url()
        try:
            response = urllib2.urlopen(req)
        except Exception,e:
            f = open(os.path.join(self.root,"pages_error.txt"),'a')
            f.write('%s---%s---%s\n' % (self.root , self.pfolder,urllib.urlencode(param)))
            f.close()
        else:
            rawdata = myutils.ungzip(response)
    #         print rawdata
            
            trs = PyQuery(rawdata.decode('utf-8'))("tr")
            for i in range(1, len(trs)):
                al = len(PyQuery(trs[i])("a"))
                if al == 3:
                    self.filename = PyQuery(PyQuery(trs[i])("a")[2]).text()
              
                    resultHref = PyQuery(PyQuery(trs[i])("a")[2]).attr("href")
    #                 self.download_result(resultHref)
                    self.get_result_page(resultHref)
                if al == 2:
                    self.filename = PyQuery(PyQuery(trs[i])("a")[1]).text()
              
                    resultHref = PyQuery(PyQuery(trs[i])("a")[1]).attr("href")                
                    self.get_result_page(resultHref)       

    
    def get_result_page(self,resultHref):
        url = "http://tongji.cnki.net/kns55/Navi/" + resultHref
       
        self.req_header["Referer"] = "http://tongji.cnki.net/kns55/Navi/result.aspx?" + resultHref
           
        req = urllib2.Request(url,None,self.req_header)
        try:
            response = urllib2.urlopen(req)
        except Exception,e:
            f = open(os.path.join(self.root,"get_result_page_error.txt"),'a')
            f.write('%s---%s---%s\n' % (self.root , self.pfolder,url ))
            f.close()
        else:
            rawdata= myutils.ungzip(response)
            pquery = PyQuery(rawdata.decode('utf-8'))

            span = pquery(ur"#ctl00_ContentPlaceHolder1_条目题名")
            if span.text().lower().rfind("excel") > 0:
                for atag in span("a"):
                    if(PyQuery(atag).text().lower().rfind("excel")) >= 0:
                         self.filename = self.filename + ".xls"
                         self.download_result(PyQuery(atag).attr("href"))
                         
                        
            else:
                for atag in span("a"):
        #             print PyQuery(atag).text()
                    if(PyQuery(atag).text().lower().rfind("pdf")) >= 0:
                        self.filename = self.filename + ".pdf"
                        self.download_result(PyQuery(atag).attr("href"))
                        
    
        
        
    def download_result(self,fileHref):
        url = "http://tongji.cnki.net/kns55" + fileHref.strip("..")
        req = urllib2.Request(url=url,data=None,headers=self.req_header)
        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar), urllib2.HTTPHandler)
        try:
            response = opener.open(req)
            if response.info().getheader("Content-Type").find("text/html") >=0: 
                data = myutils.ungzip(response).decode('utf-8')
                if data.index(u'用户登录') > 0:
                    myutils.get_cookieJar()
                    self.cookieJar = myutils.g_cookieJar
                    response = opener.open(req)
                    fname = os.path.join(os.path.join(self.root,self.pfolder), self.filename)
                    if os.path.exists(fname):
                        os.remove(fname)
                    f = open(fname,'wb')
                    f.write(response.read())
                    f.close()
    
        #     for ck in g_cookieJar:
        #         print '%s,%s' % (ck.name,ck.value)
            if response.info().getheader("Content-Type").find("pdf")>=0 or response.info().getheader("Content-Type").find("octet-stream")>=0:
                cj = copy.copy(self.cookieJar)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
                response = opener.open(req)
                fname = os.path.join(os.path.join(self.root,self.pfolder), self.filename)
                if os.path.exists(fname):
                    os.remove(fname)
                f = open(fname,'wb')
                f.write(response.read())
                f.close()
        
        except Exception,e:
            f = open(os.path.join(self.root,"download_error.txt"),'a')
            f.write('%s---%s---%s---%s\n' % (self.root , self.pfolder ,self.filename  , url ))
            f.close()
    def deal_download_error(self):
        if os.path.exists(os.path.join(self.root,"download_error.txt")):
            f = open(os.path.join(self.root,"download_error.txt"),"r+")
            lines = f.readlines()
            f.seek(0,0)
            f.truncate()
            f.close()
            for line in lines:
                words = line.strip().split('---')
                self.pfolder = words[1]
                self.filename = words[2]
                fileHref = words[3]
                self.download_result(fileHref)
                
    def deal_get_result_page_error(self):
        if os.path.exists(os.path.join(self.root,"get_result_page_error.txt")):
            f = open(os.path.join(self.root,"get_result_page_error.txt"),"r+")
            lines = f.readlines()
            f.seek(0,0)
            f.truncate()
            f.close()
            for line in lines:
                words = line.strip().split('---')
                self.pfolder = words[1]
                resultHref = words[2]
                self.download_result(resultHref)        
    
    def deal_get_child_error(self):
        if os.path.exists(os.path.join(self.root,"get_child_error.txt")):
            f = open(os.path.join(self.root,"get_child_error.txt"),"r+")
            lines = f.readlines()
            f.seek(0,0)
            f.truncate()
            f.close()
            for line in lines:
                words = line.strip().split('---')
                self.pfolder = words[1]
                param = words[2]
                self.get_child_catalog(param)
    def deal_year_error(self):
        if os.path.exists(os.path.join(self.root,"year_error.txt")):
            f = open(os.path.join(self.root,"year_error.txt"),"r+")
            lines = f.readlines()
            f.seek(0,0)
            f.truncate()
            f.close()
            for line in lines:
                words = line.strip().split('---')
                url = words[1]
                self.parse_yearbook_page(url)
                
    def deal_pages_error(self):
        if os.path.exists(os.path.join(self.root,"pages_error.txt")):
            f = open(os.path.join(self.root,"pages_error.txt"),"r+")
            lines = f.readlines()
            f.seek(0,0)
            f.truncate()
            f.close()
            for line in lines:
                words = line.strip().split('---')
                self.pfolder = words[1]
                param = words[2]
                self.pages(param) 
    def deal_error(self):
        self.deal_year_error()
        self.deal_get_child_error()
        self.deal_get_result_page_error()
        self.deal_download_error()
        self.deal_pages_error()
if __name__=="__main__":
    page =YearPage("H:\\2011")
    page.parse_yearbook_page("http://tongji.cnki.net/kns55/Navi/YearBook.aspx?id=N2011090108&floor=1")
     