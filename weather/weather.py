# coding:utf-8
import lxml.html
import urllib2
import time
import re
class Wether(object):
    def __init__(self):
        self.title = ''
        self.temp_min = ''
        self.temp_max = ''
        self.win = ''
        self.date = ''
    def __str__(self):
        return self.date+ ':'+self.title + '\n'+ '最高温度:'+ self.temp_max + '\n' +  '最底温度:'+self.temp_min + '\n' + '风级:'+self.win + '\n'



class WeeksWeather(object):
    def __init__(self,city='杭州'):
        self.city = city
        cityId = WeeksWeather.getCityId(self.city)
        self.URL = 'http://www.weather.com.cn/weather/' +str(cityId)+'.shtml'

    @classmethod
    def getCityId(cls,city=''):
        cityId = ''
        with open("weather.txt","r") as f:
            for line in f:
                t = re.split(r'[=]',line[:-1])
                if t[1] == city:
                    cityId = t[0]
                    break
        if not cityId:
            raise Exception("请输入正确的城市名称!")
        return cityId

    def down_weathers(self):  #下载天气
        Weathers = [] #保存每周的天气
        tree = lxml.html.fromstring(urllib2.urlopen(self.URL).read())
        titles = tree.xpath('//ul[@class="t clearfix"]/li/p/@title') #多云,阵雨等
        temps_mins= tree.xpath('//ul[@class="t clearfix"]/li/p[@class="tem"]/i/text()') #最底温度
        temps_maxs= tree.xpath('//ul[@class="t clearfix"]/li/p[@class="tem"]/span/text()') #最底温度
        wins = tree.xpath('//ul[@class="t clearfix"]/li/p[@class="win"]/i/text()') #风的等级
        for i in range(7):
            weather = Wether()
            weather.title = titles[i].encode('utf-8')
            if len(temps_maxs) !=7: #晚上时,网页上的最高温度就没有了,缺少数据
                temps_maxs = [u'无数据']*(7-len(temps_maxs))+temps_maxs
            weather.temp_max = temps_maxs[i].encode('utf-8')
            weather.temp_min = temps_mins[i].encode('utf-8')
            weather.win = wins[i].encode('utf-8')
            if i == 0:
                weather.date = '今天'
            elif i==1:
                weather.date = '明天'
            else:
                str = time.strftime("%w",time.localtime(time.time()+i*86400))
                if str == '0':
                    str ='天'
                weather.date = '星期' +  str
            Weathers.append(weather)
        return Weathers


if __name__=='__main__':
    w = WeeksWeather(city='杭州')
    l = w.down_weathers()
    for i in l:
        print i
    print w.URL
    print len(l)



