import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
import time

url = "http://bkjw.whu.edu.cn/servlet/b89d79056"   # 用于重定向的url
refer = 'http://bkjw.whu.edu.cn'                   # 教务系统限定了refer是这个,并且也可以作为一些请求的前半部分
s = requests.session()                             # 创建一个session
s.headers.update({"Connection": "keep-alive",\
           "Upgrade-Insecure-Requests": "1",\
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36", \
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", \
           "Referer": "http://bkjw.whu.edu.cn/stu/stu_score_parent.jsp",\
           "Accept-Encoding": "gzip, deflate",\
           "Accept-Language": "zh-CN,zh;q=0.9",\
           'referer':refer})                       # 更新headers,防反爬
           
login_data = {
"timestamp": "1610800439978",\
"jwb": "%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F",\
"id": "2019302180149",\
"pwd": "1a0a11a1093806e8883ee1f07dbb2422",\
"xdvfb": "08wm"                                    # 提交的表单的数据
}

r = s.get(url)                                     # 第一次请求获取验证码的地址
demo = BeautifulSoup(r.text,'html.parser')
a = demo.find_all('img')
checkcode_img = a[2].attrs['src']
checkcode = refer+checkcode_img                    # checkcode是验证码的网址

img = s.get(checkcode,stream=True)                 # 第二次访问下载验证码到本地并展示
with open('checkcode.gif','wb') as f:
	f.write(img.content)
image = Image.open('checkcode.gif')
image.show()

login_data['xdvfb'] = input("验证码:")              # 输入验证码并放进表单中 

JSESSION = dict(r.cookies)['JSESSIONID']
r = s.post(url,data=login_data)					   # 提交表单并且登录教务系统

url_score = 'http://bkjw.whu.edu.cn/stu/stu_score_parent.jsp'
r = s.get(url_score)                               # 访问查找成绩的网页

pattern = re.compile(r'(?<=").*?(?=")')            # 找到真正要访问的网页
demo1 = str(r.text)
url_crfs = re.findall(pattern,demo1)
url_crfs = url_crfs[73]


a = str(time.asctime())                            # 根据网页结构处理的时间
a = a.split(' ')
a[-1],a[-2] = a[-2],a[-1]
a.append('GMT+0800 (中国标准时间)')
a = ' '.join(a)

url_crfs = refer + url_crfs + a                    # 获得真正可以使用的网址

r = s.get(url_crfs)                                # 访问该网址,获得成绩信息
print(url_crfs)

demo2 = BeautifulSoup(r.text, "html.parser")       # 以下内容为用beautifulsoup提取成绩信息.

a = demo2.find_all('tr')

if len(a)== 0:
	print('未知错误') 
	
for i in a[1:]:
    all_tds = i.find_all('td')
    term = all_tds[-3].string
    year = all_tds[-4].string
    if '1' in term and '2019' in year:
        lessonName = all_tds[0].string.replace('\n', '') + '\n'
        lessonScore = all_tds[-2].string
        print(lessonName, lessonScore)





