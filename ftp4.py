
# -*- encoding: utf8 -*-
import os
import sys,string, datetime,time
from ftplib import FTP
import socket

class FTPSync(object):
    def __init__(self, rootdir_local, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.rootdir_local = rootdir_local
        self.port = port
        self.ftp = FTP()
    def login(self):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print u'开始连接到 %s' % (self.hostaddr)
            ftp.connect(self.hostaddr, self.port)
            print u'成功连接到 %s' % (self.hostaddr)
            print u' %s开始登录' % (self.username)
            ftp.login(self.username, self.password)
            print u'成功登录到 %s' % (self.hostaddr)
            debug_print(ftp.getwelcome())
        except Exception:
            print u'连接或登录失败'
        try:
            #self.ftp.cwd('/')  # 远端FTP目录
            ftp.cwd(self.remotedir)
            if not os.path.isdir(self.rootdir_local):
                os.makedirs(self.rootdir_local)
            os.chdir(self.rootdir_local)  # 本地下载目录
        except(Exception):
            print u'切换目录失败'
    def get_dirs_files(self):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.ftp.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)
    #def startbak(self):

    def walk(self, next_dir,local_dir='@$'):
        if local_dir=='@$':
            local_dir=next_dir
        print 'Walking to', next_dir.decode('utf-8')
        self.ftp.cwd(next_dir)
        try:
            os.mkdir(local_dir.decode('utf-8'))
        except OSError:
            pass
        t = local_dir.decode('utf-8')
        print t
        os.chdir(t)

        ftp_curr_dir = self.ftp.pwd()
        local_curr_dir = os.getcwd()

        files, dirs = self.get_dirs_files()
        print "FILES: ", files
        print "DIRS: ", dirs
        #将每个目录层中的文件先下载，再遍历目录
        for f in files:
            print local_curr_dir,'正在保存',next_dir, '目录下的:', f
            outf = open(f.decode('utf-8'), 'wb')
            try:
                self.ftp.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        for d in dirs:
            print '切换目录至：',local_curr_dir
            os.chdir(local_curr_dir)
            self.ftp.cwd(ftp_curr_dir)
            #递归调用遍历每一层目录.
            self.walk(d)
    def run(self):
        self.walk(self.remotedir,self.rootdir_local)
        #self.walk('.')

def main(rootdir_local, hostaddr, username, password, remotedir, port):
    f = FTPSync(rootdir_local, hostaddr, username, password, remotedir, port)
    f.login()
    f.run()
def get_serverlist():
    print u'从 %s 中读取服务器列表' % (local_file_list_txt)
    try:
        fileTxt = open(local_file_list_txt, 'r')
    except Exception, e:
        print e
    for line in fileTxt:
        if '\xef\xbb\xbf' in line:
            line = line.replace('\xef\xbb\xbf', '')  # 用replace替换掉'\xef\xbb\xbf'
        line = line.strip('\n')
        line = line.strip(' ')
        local_files.append(line)
if __name__ == '__main__':

    print '''
             *************************************
             **       Welcome to use XPftp     **
             **      Created on  2017-06-18     **
             **       @author: peeperp            **
             *************************************
          '''
    #time.sleep(2000)
    chioes = raw_input('Please enter your selection, 1 backup, 2 upload, 3 exit: ')
    if chioes=='1':
        file = open("log.txt", "a")
        timenow = time.localtime()
        datenow = time.strftime('%Y-%m-%d', timenow)
        logstr = datenow
        rootdir_local = 'E:/temp/12'  # 本地目录
        rootdir_remote = '/'  # 远程目录
        local_file_list_txt = 'E:/temp/12/fileList.txt'  # 配置文件
        local_files = []
        get_serverlist()
        print '本次备份服务器列表', local_files
        for ser in local_files:
            ser = eval(ser)
            print "开始备份：" + ser["name"]
            hostaddr = ser["hostaddr"]  # ftp地址
            username = ser["username"]  # 用户名
            password = ser["password"]  # 密码
            port = ser["port"]  # 端口号
            rootdir_local = ser["localdir"]  # 本地目录
            rootdir_remote = ser["remotedir"]  # 远程目录
            main(rootdir_local, hostaddr, username, password, rootdir_remote, port)
        timenow = time.localtime()
        datenow = time.strftime('%Y-%m-%d', timenow)
        logstr += " - %s 成功执行了备份\n" % datenow
        debug_print(logstr)

        file.write(logstr)
        file.close()
    elif chioes == '2':
        print 'Function is under development!'
    else:
        print 'Error input!'
        sys.exit(-1)

    '''配置文件格式
    #{'name':'server1','hostaddr':'202.101.231.234','username':'testpython','password':'test123@321','port':21,'remotedir':'.','localdir':'E:/temp/12/ftp/1/'}
    #{'name':'server2','hostaddr':'202.101.231.234','username':'testpython2','password':'test123@321','port':21,'remotedir':'.','localdir':'E:/temp/12/ftp/2/'}
    #{'name':'server3','hostaddr':'202.101.231.234','username':'testpython3','password':'test123@321','port':21,'remotedir':'.','localdir':'E:/temp/12/ftp/3/'}
    '''
