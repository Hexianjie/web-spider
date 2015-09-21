# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib
import time
class Mailhelper(object):
    '''
    这个类实现发送邮件的功能
    '''
    def __init__(self,mailto_list):

        self.mail_host="smtp.sina.cn"  #设置服务器
        self.mail_user="14778860037m0"    #用户名
        self.mail_pass="exiangjie"   #密码
        self.mail_postfix="sina.cn"  #发件箱的后缀
        self.mailto_list = mailto_list  #收件箱的后缀


    def send_mail(self,title,content):
        me="我是快乐的小脚本~"+"<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = ";".join(self.mailto_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, self.mailto_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False

if __name__ == '__main__':
    mailto_list=['hexianjie1995@qq.com'] #此处填写接收邮件的邮箱
    title = "标题~"
    content = '内容'
    mail = Mailhelper(mailto_list)
    if mail.send_mail(title,content):
        print u"发送成功"
    else:
        print u"发送失败"