import smtplib
from email.mime.text import MIMEText


class SendEmail(object):
    def __init__(self, information):
        self.grade_information = information
        self.msg = MIMEText(self.grade_information, "plain", "utf-8")
        self.from_addr = "2431340038@qq.com"
        self.from_pwd = "xxxxxxxxxxxxxx"   # 这里输入的是你的邮箱的授权码, 不是真的密码
        self.to_addr = "2431340038@qq.com"
        self.smtp_srv = "smtp.qq.com"
        self.subject = "出成绩了xd"
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.from_addr
        self.msg['To'] = self.to_addr

    def Send(self):
        try:
            srv = smtplib.SMTP_SSL(self.smtp_srv.encode(), 465)
            srv.login(self.from_addr, self.from_pwd)
            srv.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
            print('发送成功!!!!')
        except Exception as e:
            print('发送失败!!!!')
        finally:
            # 无论发送成功还是失败都要退出你的QQ邮箱
            srv.quit()

