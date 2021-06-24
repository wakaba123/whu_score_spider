# whu_score_spider
 spider for getting final score

本爬虫仅供交流学习使用

如需使用成绩查询功能
请自行再浏览器中抓取登录时加密后的密码并且在25,26行替换

2020年1月18日下午15:41更新<br>
原来老教务系统的加密就是一个简单的md5加密<br>
就这?就这?<br>
所以只需要在代码中填上自己的学号和密码和要查询的学年和学期就行

新教务系统可是rsa加密啊<br>
<br>

第99行和第100行填入自己的学号和密码
需要自行安装PIL库,beautifulsoup库和requests库
