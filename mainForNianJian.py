#coding=utf-8
import NianJian
import socket,sys
import myutils



reload(sys)

sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(120)


if __name__ == "__main__":
    try:
        file = open("data/nianjians.txt",'r')
    except Exception,e:
        print "years.txt doesn't exist!"
    else:
        lines = file.readlines()
        for line in lines:
            words = line.strip().split("---")
            NianJian.NianJian(words[0].decode('utf-8'),words[1].decode('utf-8')).start()
        file.close()