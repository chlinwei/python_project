#coding:utf-8
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
import smtplib
from weather import WeeksWeather 
import sys 

class Sender(object):
    def __init__(self,from_addr,password,smtp_host='',port=''):
        self.from_addr = from_addr
        self.password = password
        self.smtp_host = smtp_host
        self.port = port
        if not smtp_host:
            self.smtp_host = 'smtp.' + re.split('[@\.]',self.from_addr)[1] + '.com' 
        if not port:
            self.port = 25

        
    def send(self,to_addr):
        if len(sys.argv)==1:
            raise Exception("请输入城市名称额:")
        w = WeeksWeather(sys.argv[1])
        weathers = w.down_weathers()
        s = ''
        for i in weathers:
            s += str(i) + '#'*10 + '\n'*2 + '<br>'
        s = '<html><body>' + s + '</body></html>'
	msg = MIMEText(s,'html','utf-8') #注意这里用html不然发不出去
	msg['From'] = self.from_addr
	msg['To'] =  to_addr
	msg['Subject'] = Header('来自SMTP的问候...','utf-8').encode()
	server = smtplib.SMTP(self.smtp_host,25)
	# server.starttls() #加密
	#server.set_debuglevel(1) #调试信息
	server.login(self.from_addr,self.password)
	server.sendmail(self.from_addr,[to_addr],msg.as_string())
	server.quit()





if __name__=='__main__':
    from_addr = 'm15345710576@163.com'
    password = 'linwei359'
    s = Sender(from_addr,password)
    s.send('862350707@qq.com')


