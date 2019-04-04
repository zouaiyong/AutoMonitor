# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 10:12
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : dataTemplate.py
# @Software: PyCharm
class DataTemplate:

    # data数据模板
    # 程序运行得到的数据将不再存放到txt文件中，而是存放到此模板中，即内存中

    def __init__(self, strDateTime):
        # 添加标识self.strServerName-add in 2018-04-09

        self.dataForHour = ""
        self.dataForSecond = ""
        self.dataAll = ""
        self.detailAll=''
        self.strDateTime = strDateTime

    def createDictTextData(self):
        # 创建一个普通的文本dict数据，并返回

        strDataContent = (self.dataAll + "\n\n" + self.strDateTime + "监控发布")

        dictData = {
            "msgtype": "text",
            "text": {
                "content": strDataContent
            },
            "isAtAll": 'false'
        }
        return dictData

    def createMarkdownData(self):
        # 创建一个markdown语法的dict数据，并返回

        strDataContentMark = (self.dataAll + "\n\n > " + " ##### " + self.strDateTime + " 监控发布")

        dictData = {
            "msgtype": "markdown",
            "markdown": {
                "title": "监控服务",
                "text": "### [监控服务]\n >" + strDataContentMark
            },
            "at": {
                "isAtAll": 'false'
            }
        }
        return dictData
