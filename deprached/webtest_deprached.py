# -*- coding: utf-8 -*-
import sys,string,random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

global g_cookie

class BrowserWidget(QWidget):
    def __init__(self,HOMEPAGE,parent=None):
        super(self.__class__, self).__init__(parent)
        self.browser = QWebView()
        self.lineedit = QLineEdit()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.connect(self.lineedit, SIGNAL("returnPressed()"), self.entrytext)

        self.browser.load(QUrl(HOMEPAGE))
        self.browser.show()

    def entrytext(self):
        self.browser.load(QUrl(self.lineedit.text()))
    
    def CookieOk(self):
        self.cookies = {}
        for citem in self.browser.page().networkAccessManager().cookieJar().allCookies():
            self.cookies['%s'% (citem.name())]= '%s'%(citem.value())
#             print '%s=%s' % (citem.name(), citem.value())
        #self.cookies = common.to_unicode('; '.join(self.cookiescookies))
        global g_cookie
        g_cookie = self.cookies
        
    
class Window(QMainWindow):
    def __init__(self,TITLE,HOME,parent=None):
        super(self.__class__, self).__init__(parent)
        self.browserWindow = BrowserWidget(HOME)
        self.setCentralWidget(self.browserWindow)
        self.setWindowTitle(TITLE)

        status = self.statusBar()
        status.setSizeGripEnabled(True)
        self.label = QLabel("")
        status.addWidget(self.label, 1)

        self.connect(self.browserWindow.browser, SIGNAL("loadStarted(bool)"), self.loadStarted)
        self.connect(self.browserWindow.browser, SIGNAL("loadFinished(bool)"), self.loadFinished)
        self.connect(self.browserWindow.browser, SIGNAL("loadProgress(int)"), self.loading)
        
        self.loginFlag = 1

    def loadStarted(self, flag):
        print 'requestedUrl:' + self.browserWindow.browser.page().mainFrame().requestedUrl()
    def loadFinished(self, flag):
        
        if 'http://tongji.cnki.net/kns55/brief/login/login.aspx?type=login' == str(self.browserWindow.browser.url().toString()) and self.loginFlag:

          
            frame = self.browserWindow.browser.page().mainFrame()
            #print doc.toPlainText().toUtf8()
            doc = frame.documentElement()
            #m_blog = doc.findFirst("#form1")
            #print m_blog.toPlainText().toUtf8()
    
         
            nameInput = doc.findFirst('input[id="username"]')
            #nameInput = doc.findFirst('#TANGRAM__3__userName')
            nameInput.setAttribute('value',u'zky311053')
            passwordInput = doc.findFirst('input[id="password"]')
            passwordInput.setAttribute('value',u'123456')
    
            loginBtn = doc.findFirst('input[id="ImageButton1"]')
            loginBtn.evaluateJavaScript("this.click()")
    
            self.loginFlag = 0
            
        if 'http://tongji.cnki.net/kns55/brief/login/login.aspx?type=login' != str(self.browserWindow.browser.url().toString()):
            self.browserWindow.CookieOk()
            self.close()
            
    def loading(self, percent):
        self.browserWindow.lineedit.setText(self.browserWindow.browser.url().toString())
    
    def return_cookie(self):
        return self.browserWindow.CookieOk()
def main():
    app = QApplication(sys.argv)
    window = Window(TITLE = u"BaiduLogin",HOME = "http://tongji.cnki.net/kns55/brief/login/login.aspx?type=login")
#     window.show()
    app.exec_()
    app.exit()
#     sys.exit()

