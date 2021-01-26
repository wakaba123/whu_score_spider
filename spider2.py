import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
import time
import os


class Spider(object):
    def __init__(self):
        self.url = "http://bkjw.whu.edu.cn/servlet/_6daf195df2a"  # 用于重定向的url
        self.refer = 'http://bkjw.whu.edu.cn'  # 教务系统限定了refer是这个,并且也可以作为一些请求的前半部分
        self.s = requests.session()
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
            "id": "2019302180149",
            "pwd": "1a0a11a1093806e8883ee1f07dbb2422",
            "xdvfb": ""  # 提交的表单的数据
        }

    def getCaptcha(self):
        r = self.s.get(self.url)  # 第一次请求获取验证码的地址
        demo = BeautifulSoup(r.text, 'html.parser')
        a = demo.find_all('img', attrs={'name': "sleep"})
        print(a)
        captcha_img = a[0].attrs['src']

        captcha = self.refer + captcha_img  # checkcode是验证码的网址
        # print(captcha)
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
        r = self.s.post(self.url, data=self.login_data)
        if len(r.text) != 17906:
            print(r.text)
            return False
        else:
            im = Image.open('checked.gif')
            im.save(self.login_data['xdvfb'] + '.tiff')
            os.remove('checked.gif')
            return True

    def getScorePage(self):
        url_score = 'http://bkjw.whu.edu.cn/stu/stu_score_parent.jsp'
        r = self.s.get(url_score)  # 访问查找成绩的网页

        pattern = re.compile(r'(?<=\").*?(?=\")')  # 找到真正要访问的网页
        demo1 = str(r.text)
        url_crfs = re.findall(pattern, demo1)
        url_crfs = url_crfs[73]

        a = str(time.asctime())  # 根据网页结构处理的时间
        a = a.split(' ')
        a[-1], a[-2] = a[-2], a[-1]
        a.append('GMT+0800 (中国标准时间)')
        a = ' '.join(a)

        url_crfs = self.refer + url_crfs + a  # 获得真正可以使用的网址
        print(url_crfs)
        r2 = self.s.get(url_crfs)  # 访问该网址,获得成绩信息
        return r2.text

    def processScore(self, year, term):
        demo2 = BeautifulSoup(self.getScorePage(), "html.parser")  # 以下内容为用beautifulsoup提取成绩信息.
        score_not_got = 0
        a = demo2.find_all('tr')
        if len(a) == 0:
            print('未知错误')
        for i in a[1:]:
            all_tds = i.find_all('td')
            termData = all_tds[-3].string
            yearData = all_tds[-4].string
            if term in termData and year in yearData:
                lessonName = all_tds[0].string.replace('\n', '') + '\n'
                lessonScore = all_tds[-2].string
                if lessonScore is None:
                    score_not_got += 1
                print(lessonName, lessonScore)
        return score_not_got


spider = Spider()

# while True:
#     spider.login()

while spider.login() is False:
    pass

while True:
    year = '2020'
    term = '1'
    print("没出的成绩有%d门" % spider.processScore(year, term))
    print(time.asctime())
    time.sleep(300)
