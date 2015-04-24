import cookielib
import sqlite3
import win32crypt
# import urllib2, urllib
# from pyquery import PyQuery
def ungzip(response):
    header = response.info()
    rawdata = response.read()
    
    if header.get("Content-Encoding") == 'gzip':
        import gzip
        import StringIO
        data = StringIO.StringIO(rawdata)
        gz = gzip.GzipFile(fileobj=data)
        rawdata = gz.read()
        gz.close()
    return rawdata

def get_cookieJar():
    readCookieFromChrome()
    file = open("data/chrome_cookies.txt",'r')
    lines = file.readlines()
    cj = cookielib.CookieJar()
    for line in lines:
        line = line.strip()
        c = cookielib.Cookie(None,line.split(";")[1].split(":")[1],line.split(";")[2].split(":")[1],None, False,".cnki.net",True, False, '/', True, False, None, False, None, None, None)
        cj.set_cookie(c)
    return cj

def readCookieFromChrome():
    outFile_path=r'data/chrome_cookies.txt';
    sql_file= r'data/Cookies';
    sql_exe="select host_key,name,value,encrypted_value from cookies where host_key='.cnki.net' or host_key='tongji.cnki.net'";
    conn = sqlite3.connect(sql_file)
    outFile = open(outFile_path,'w')
    for row in conn.execute(sql_exe):
        pwdHash = str(row[3])
        try:
            ret = win32crypt.CryptUnprotectData(pwdHash, None, None, None, 0)
        except:
            print 'Fail to decrypt chrome cookies'
            sys.exit(-1)
        outFile.write('host_key:{0};name:{1};value:{2}\n'.format(row[0], row[1],ret[1]))
    outFile.close()
    conn.close()
#     print 'All Chrome cookies saved to:\n' + outFile_path
    
def filenameCheck(filename):
    illeagal = [u"\\",u"/",u":",u"?",u'"',u"<",u">",u"|",u"*"]
    for s in illeagal:
        filename = filename.replace(s,"")
    return filename


    
