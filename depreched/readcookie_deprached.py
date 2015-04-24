import sqlite3
import win32crypt
def readCookieFromChrome():
    outFile_path=r'chrome_cookies.txt';
    sql_file= r'Cookies';
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
    print 'All Chrome cookies saved to:\n' + outFile_path