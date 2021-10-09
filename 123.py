from send_mail import SendEmail
from spider2 import Spider
import time

if __name__ == '__main__':
    id = '2019302180149'  # 这里输入你的学号
    pwd = 'xxxxxx'  # 这里输入你的密码
    year = '2020'  # 这里输入查询的年份
    term = '2'  # 这里输入查询的学期
    spider = Spider(id, pwd, year, term)
    score_not_get = 0

    while spider.login() is False:
        pass

    while True:
        temp = spider.processScore()
        if temp != score_not_get:
            information = "成绩新出了"+str(score_not_get-temp)+"门"
            send = SendEmail(information)
            send.Send()
            score_not_get = temp
        print("没出的成绩有%d门" % score_not_get)
        print(time.asctime())
        time.sleep(300)
