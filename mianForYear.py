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


if __name__=="__main__":
    try:
        file = open("data/years.txt",'r')
    except Exception,e:
        print "years.txt doesn't exist!"
    else:
        lines = file.readlines()
        for line in lines:
            words = line.strip().split("---")
            YearPage(words[0].decode('utf-8'),words[1].decode('utf-8')).start()
        file.close()