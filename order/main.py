# coding:utf-8
#author:linwei
import urllib2
import urllib
import cookielib
import lxml.html
import datetime
import pickle
import re
import os

class Person(object):
    POST_URL = 'http://kc.zj.com/my/user_select_new.php'
    LOGIN_URL = 'http://kc.zj.com/my/login_new.php '
    def __init__(self,username,password,Sat=False):
        self.username = username
        self.Sat = Sat
        self.password = password
        self.opener = self.__get_opener()
        #下个月的MAIN_PAGE的URL
        self.NEXT_MONTH_URL = ''
        #刚登陆进去的点餐界面
        self.MAIN_PAGE = ''
        # 本周的选择订餐界面的url
        self.weekLinks = []
        #本周的起始天和结束天
        self.weekdays = self.__get_weeks()
    #本周�所有post参数
        self.pages = []
    def __get_opener(self):
        cookie = cookielib.CookieJar()
        opener =  urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.add_handler=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')]
        return opener
    def login(self):
        data = {
            'loginsubmit.x': '24',
            'loginsubmit.y': '25',
            'username':self.username,
            'password':self.password
        }
        try:
            self.opener.open(Person.LOGIN_URL,urllib.urlencode(data)).read()
        except urllib2.URLError as e:
            if e.reason:
                print e.reason
            else:
                raise Exception('login error')
        self.MAIN_PAGE = self.opener.open(Person.POST_URL).read()
        e = lxml.html.fromstring(self.MAIN_PAGE)
        trs = e.xpath('//table[@class="TdPadding"]/tbody/tr[1]/td/a[@href]')
        self.NEXT_MONTH_URL = "http://kc.zj.com/my/" + trs[1].get('href')
        # 本周的选择订餐界面的url
        links = e.xpath('//table[@class="TdPadding"]/tbody/tr[position()>2]/td/a')
        divs = e.xpath('//table[@class="TdPadding"]/tbody/tr[position()>2]/td/a/div/text()')
        for i in range(len(links)):
            if Person.__parse_Int(divs[i]) in self.weekdays:
                self.weekLinks.append('http://kc.zj.com/my/user_select_new.php' + links[i].get('href'))
         #本周所有post参数
        self.pages = self.__get_pages()

    def order(self):
        for page in self.pages:
            data = { '_client':page['_client']}
            for i in range(7):
                if len(page['items'])!=7 and i==3:
                    break
                d = {page['items'][i]['shopID']:page['items'][i]['value']}
                if i==2:
                    d = {page['items'][i]['shopID']:page['items'][i]['value'],'pid':page['items'][i]['pid']}
                data.update(d)
            self.opener.open(Person.POST_URL,data=urllib.urlencode(data))


    def __get_pages(self):
        pages = []
        for href in self.weekLinks:
            h = self.opener.open(href).read()
            p = r'name=\"_client\" value=\"(.*?)\"'
            m =  re.search(p,h)
            items = []
            if m:
                _client = m.group(1)
                e = lxml.html.fromstring(h)
                tables = e.xpath('//div[@class="listbd2"]/table/tr/td/table//table')
                for table in tables: #7个table
                    inputs = table.xpath("tr/td/input") #2个input
                    item = {'shopID':inputs[1].get('name'),'value':inputs[1].get('value'),'pid':inputs[0].get('value')}
                    items.append(item)
                page = {'_client':_client,'items':items}
                pages.append(page)
        return pages


    @staticmethod
    def __parse_Int(s):
        s1 = ''
        for i in s:
            if '0' <= i <= '9':
                s1 += i
            else:
                if s1:
                    return int(s1)
                else:
                    raise (Exception("s1 is not convert to int"))
    def __get_weeks(self):
        """
        :return: 返回本周的第一天到最后一天
        """
        vdate = datetime.datetime.now()
        dayscount = datetime.timedelta(days=vdate.isoweekday())
        dayfrom = vdate - dayscount + datetime.timedelta(days=1)
        dayto = dayfrom + datetime.timedelta(days=4)
        if self.Sat:
            if os.path.exists('data.pkl'):
                f = open("data.pkl")
                data = pickle.load(f)
                f.close()
                f = open("data.pkl", "wb")
                if data == 1:
                    dayto = dayto + datetime.timedelta(days=1)
                    data = 0
                    pickle.dump(data, f)
                else:
                    data = 1
                    pickle.dump(data, f)
                f.close()
            else:
                f = open("data.pkl", "wb")
                data = 1
                dayto = dayto + datetime.timedelta(days=1)
                pickle.dump(data, f)
                f.close()
        else:
            if os.path.exists('data.pkl'):
                os.remove('data.pkl')
        return range(dayfrom.day, dayto.day + 1)

#点的全是餐券
#如果周六要点餐,则Sat设置为True就可以了
p = Person(username='xxxxxx',password='xxxxx',Sat=True)
p.login()
p.order()
