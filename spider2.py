import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
import time
import hashlib


class Spider(object):
    def __init__(self, your_id, your_pwd, year, term):
        self.url = "http://bkjw.whu.edu.cn/servlet/_6daf195df2a"  # 用于重定向的url
        self.refer = 'http://bkjw.whu.edu.cn'  # 教务系统限定了refer是这个,并且也可以作为一些请求的前半部分
        self.s = requests.session()
        self.id = your_id
        self.pwd = your_pwd
        self.s.headers.update({"Connection": "keep-alive",
                               "Upgrade-Insecure-Requests": "1",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                             "like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                                         "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                               "Accept-Encoding": "gzip, deflate",
                               "Accept-Language": "zh-CN,zh;q=0.9",
                               'Referer': self.refer})  # 更新headers,防反爬
        self.login_data = {
            "timestamp": "1610880036436",
            "jwb": "%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F",
            "id": self.id,
            "pwd": self.getHashPwd(),
            "xdvfb": ""  # 提交的表单的数据
        }
        self.queryinfo = {
            "term": term,
            "year": year
        }
        #self.proxies = { "http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080", }
        self.proxies = {}

    def getHashPwd(self):
        return hashlib.md5(self.pwd.encode(encoding='UTF-8')).hexdigest()

    def getCaptcha(self):
        r = self.s.get(self.url)  # 第一次请求获取验证码的地址
        demo = BeautifulSoup(r.text, 'html.parser')
        a = demo.find_all('img', attrs={'name': "sleep"})
        captcha_img = a[0].attrs['src']
        captcha = self.refer + captcha_img  # checkcode是验证码的网址
        return captcha

    def inputCaptcha(self):
        img = self.s.get(self.getCaptcha(), stream=True)  # 第二次访问下载验证码到本地并展示
        with open('checked.gif', 'wb') as f:
            f.write(img.content)
        image = Image.open('checked.gif')
        image.show()
        self.login_data['xdvfb'] = input("验证码:")  # 输入验证码并放进表单中

    def login(self):
        self.inputCaptcha()
        r = self.s.post(self.url, data=self.login_data, proxies=self.proxies)  # zheli
        pattern1 = "验证码错误"
        pattern2 = "密码错误"
        if re.search(pattern1, str(r.text)):
            print("验证码错误")
            return False
        elif re.search(pattern2, str(r.text)):
            print("用户名/密码错误")
            a = input("xd快去文件里改密码")
        else:
            return True

    def getScorePage2(self):
        url = self.refer + '/servlet/Svlt_QueryStuScore'
        r = self.s.post(url, data=self.queryinfo, proxies=self.proxies)
        return r.text

    def processScore(self):
        demo2 = BeautifulSoup(self.getScorePage2(), "html.parser")  # 以下内容为用beautifulsoup提取成绩信息.
        score_not_got = 0
        a = demo2.find_all('tr')
        if len(a) == 0:
            print('未知错误')
        for i in a[1:]:
            all_tds = i.find_all('td')
            termData = all_tds[-3].string
            yearData = all_tds[-4].string
            lessonName = all_tds[0].string.replace('\n', '') + '\n'
            lessonScore = all_tds[-2].string
            if lessonScore is None:
                score_not_got += 1
            print(lessonName, lessonScore)
        return score_not_got


id = '2019302180xxx'  # 这里输入你的学号
pwd = 'xxx'  # 这里输入你的密码
year = '2020'  # 这里输入查询的年份
term = '2'  # 这里输入查询的学期
spider = Spider(id, pwd, year, term)

while spider.login() is False:
    pass

while True:
    print("没出的成绩有%d门" % spider.processScore())
    print(time.asctime())
    time.sleep(300)
