import cookielib
import urllib2, urllib
from pyquery import PyQuery
import webtest2


g_cookieJar = None

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
    webtest2.main()
    webtest2.g_cookie
    cj = cookielib.CookieJar()
    for key in webtest2.g_cookie.keys():
        c = cookielib.Cookie(None,key,webtest2.g_cookie[key],None, False, '.cnki.net',True, False, '/', True, False, None, False, None, None, None)
        cj.set_cookie(c)
    global g_cookieJar
    g_cookieJar = cj
    
    
    

    
