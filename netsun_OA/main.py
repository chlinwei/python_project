#coding:utf-8
import urllib
import urllib2
import cookielib
import re
from PIL import Image
import pytesseract

HOMEPAGE='https://www2.netsun.com/prog/index.cgi'
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.add_handler = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36')]

html = opener.open(HOMEPAGE).read()


def filter_image(im):
    im2 = Image.new("P",im.size,255)
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            if pix == 101:
                im2.putpixel((y,x),0)
    return im2

    
def get_v_secret():
    p = r'id=\"chk_img\" src=\"(.*?)\"'
    img_URL = 'https://www2.netsun.com'+re.search(p,html).group(1)
    im = opener.open(img_URL)
    im = Image.open(im)
    im2 = filter_image(im)
    return pytesseract.image_to_string(im2)

def get_v_id():
    p = r'name=v_id value=\"(.*?)\"'
    return re.search(p,html).group(1)


def get_v_digest():
    p = r'name=v_digest value=\"(.*?)\"'
    return re.search(p,html).group(1)

data = {
    'f':'login',
    'returl':'',
    'username':'130296',
    'submit.x':28,
    'submit.y':22,
    'password':'130296',
    'v_id':get_v_id(),
    'v_digest':get_v_digest(),
    'v_secret':get_v_secret(),
}
POST_URL = 'https://www2.netsun.com/prog/index.cgi'
response  = opener.open(POST_URL,urllib.urlencode(data))
WAGE='https://www2.netsun.com/prog/Action.cgi?t=my_wage'
with open("a.html","w") as f:
    f.write(opener.open(WAGE).read())

