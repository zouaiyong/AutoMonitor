# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:12
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : operate.py
# @Software: PyCharm
from model.util.dingTalk import ResponseDD
from model.util.emailUtil import EmailUtil
from model.FUNC.getEmailInfo import *
from model.FUNC.dbCheck import *


class Operate():

    # 选择执行操作类

    def __init__(self,dictMsgRun):
        """
        :param dictMsgRun: [{"task_id":"","case_result":"","case_level":"","email_id":""}]
        """
        # self.dictMsgRun = readConfigureFile()
        self.dictMsgRun = dictMsgRun
        self.EmailInfo = Email_Info()
        self.dataTemplateObj = DataTemplate(
            RunTime().getDateTime())
        self.runProcess()

    def runProcess(self):

        # 运行检测各个项目
        # dictMsgRun: 需要运行的数据项目
        for i in self.dictMsgRun:
            Get_DB_Keyword(i,self.dataTemplateObj)
        # SqlCheck(self.dictMsgRun, self.dataTemplateObj)
            for j in self.EmailInfo:
                self.choiceSendMsgMethod(eval(j))

        # resultdata = monitor_log()
        # self.dataTemplateObj = DataTemplate(RunTime().getDateTime())
        # self.dataTemplateObj.dataAll = resultdata
        # self.dataTemplateObj.detailAll = "<h2>" + "监控到日志含有关键字的内容如下：" + "</h2>" + "<br>" + str(resultdata)
        # for i in range(len(self.EmailInfo)):
        #     self.choiceSendMsgMethod(eval(self.EmailInfo[i]))
        #ResponseDD(dataTemplate, self.dictMsgRun)

    def choiceSendMsgMethod(self, dictNeedRunMsg):
        # 根据配置文件来选择使用email或者dingtalk来发送消息
        if('email' in dictNeedRunMsg):
            if(dictNeedRunMsg.get('email') == 'yes'):
                pass
                emailUtil = EmailUtil(dictNeedRunMsg,self.dataTemplateObj)
            else:
                print("不执行email服务", 'runLog')

        if('dingtalk' in dictNeedRunMsg):
            if(dictNeedRunMsg.get('dingtalk') == 'yes'):
                responseDD = ResponseDD(self.dataTemplateObj, dictNeedRunMsg)
                pass
            else:
                print("不执行钉钉服务", 'runLog')
        else:
            print("不执行钉钉服务", 'runLog')


if __name__ == "__main__":
    a = ["TASK_201808201944370021"]
    Operate(a)
