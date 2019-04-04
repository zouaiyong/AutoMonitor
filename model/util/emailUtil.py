# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 10:12
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : emailUtil.py
# @Software: PyCharm
import os
import sys
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class EmailUtil:

    # 发送邮件模块

    def __init__(self, dictNeedRunMsg, dataTemplateObj):

        # dictNeedRunMsg:存放从配置文件中读取到的数据，其数据是本次检测运行所需要的数据
        # 该数据仅进行了初步过滤
        # dataTemplateObj: DataTemplate的对象(脚本从运行到结束都只有这一个DataTemplate对象)
        # 其中的key有
        # smtp_server:
        # mail_sendAddr:
        # mail_sendPasswd:
        # mail_toAddr:
        self.dataTemplate=dataTemplateObj
        dictEmailMsg = self.getForEmailMsg(dictNeedRunMsg)

        if((len(dictEmailMsg) == 1) and ('err' in dictEmailMsg)):
            print("邮件发送配置不全,发送邮件任务运行中止")
        else:
            strData = self.dataTemplate.dataAll
            print(strData)
            if (strData == ""):
                print("数据为空,将不执行执行发送邮件任务")
            else:
                print("-->执行邮件服务")
                listEmailContentMsg = self.getEmailContentMsg()
                self.choiceSend(dictEmailMsg, listEmailContentMsg)


    def getForEmailMsg(self, dictNeedRunMsg):

        # 将从配置文件的完全读取到的数据中，抽取出发送邮件需要的数据，存放为dict类型并返回
        # dictNeedRunMsg: 存放从配置文件中读取到的数据，其数据是本次检测运行所需要的数据
        # 因为有可能并不是所有项目都配置了需要运行

        dictMsgForEmail = {}
        for keyItem in dictNeedRunMsg:
            if((keyItem == 'email_sendaddr') | (keyItem == 'email_sendpasswd') |
               (keyItem == 'smtp_server') | (keyItem == 'ToEmail')):
                if(dictNeedRunMsg.get(keyItem) != ''):
                    dictMsgForEmail[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForEmail.clear()
                    dictMsgForEmail['err'] = "Msg Incomplete"
                    break

        return dictMsgForEmail

    def getEmailContentMsg(self,sendFilePath=None,senFile=False):
        dictEmailContentMsg={}
        dictEmailContentMsg['byFile']=senFile
        dictEmailContentMsg['strSubject']='【监控告警】'
        dictEmailContentMsg['strContent']='<html xmlns="http://www.w3.org/1999/xhtml"><head><body>\n'+self.dataTemplate.detailAll+'</body></html>'
        print(self.dataTemplate.detailAll)
        dictEmailContentMsg['filePath']=sendFilePath
        return dictEmailContentMsg
    def choiceSend(self, dictEmailMsg, dictEmailContent):

        # 选择发送类型(有无附件)
        # dictEmailMsg: 发送和接受邮件账户，及smtp服务器地址
        # dictEmailContent: 发送的邮件内容，主题，附件

        strSmtpServer = dictEmailMsg.get('smtp_server')
        strSendAddr = dictEmailMsg.get('email_sendaddr')
        strPasswd = dictEmailMsg.get('email_sendpasswd')
        listToAddr = dictEmailMsg.get('ToEmail')
        CCToAddr = dictEmailMsg.get('CcEmail')
        strSubject = dictEmailContent.get('strSubject')
        strContent = dictEmailContent.get('strContent')
        if(dictEmailContent.get('byFile')):
            strErrFilePath = dictEmailContent.get('filePath')
            self.sendEmailByStringAndFile(
                strSmtpServer,
                strSendAddr,
                strPasswd,
                listToAddr,
                CCToAddr,
                strSubject,
                strContent,
                strErrFilePath)
        else:
            self.sendEmailByString(strSmtpServer, strSendAddr, strPasswd,
                                   listToAddr, CCToAddr,strSubject, strContent)




    def sendEmailByString(self, strSmtpServer, strSendAddr, strPasswd,
                          listToAddr,CCToAddr, strSubject, strContent):

        # 用字符串来发送邮件
        # strSmtpServer: smtp服务器地址
        # strSendAddr: 邮件发送地址
        # strPasswd: 发送地址的登陆授权码
        # listToAddr: 接受邮件的地址，为list集合
        # strSubject: 邮件主题
        # strContent: 邮件内容字符串类型

        message = MIMEText(strContent, "html", "utf-8")
        message['Subject'] = Header(strSubject, 'utf-8')
        message['From'] = Header('<%s>' % strSendAddr, 'utf-8')
        message['To'] = Header(str(listToAddr),'utf-8')
        if CCToAddr != None:
            message['Cc'] = Header(str(CCToAddr), 'utf-8')

        try:
            smtpObj = SMTP_SSL(strSmtpServer)
            smtpObj.set_debuglevel(1)
            smtpObj.ehlo(strSmtpServer)
            smtpObj.login(strSendAddr, strPasswd)
            print("登陆成功", 'runLog')
            if(CCToAddr != None and listToAddr != None) :
                print("抄送地址不为空")
                print(listToAddr)
                print(CCToAddr)
                print(listToAddr.split(",") + CCToAddr.split(","))
                smtpObj.sendmail(strSendAddr, listToAddr.split(",") + CCToAddr.split(","), message.as_string())
                smtpObj.quit()
            elif(CCToAddr == None and listToAddr != None) :
                print("抄送地址为空")
                print(listToAddr)
                print(CCToAddr)
                smtpObj.sendmail(strSendAddr, listToAddr, message.as_string())
                smtpObj.quit()

            else:
                print("接收邮件地址为空")
                print("邮件不发送")
        except BaseException as e:
                print(e)
                print(sys.exc_info()[0])
                print("邮件发送失败")

    def sendEmailByStringAndFile(
            self,
            strSmtpServer,
            strSendAddr,
            strPasswd,
            listToAddr,
            CCToAddr,
            strSubject,
            strContent,
            strErrFilePath):

        # 发送有附件的邮件
        # strSmtpServer: smtp服务器地址
        # strSendAddr: 邮件发送地址
        # strPasswd: 发送地址的登陆授权码
        # listToAddr: 接受邮件的地址，为list集合
        # strSubject: 邮件主题
        # strContent: 邮件内容字符串类型
        filename=strErrFilePath.split(os.sep)[-1]
        message = MIMEMultipart()
        message['Subject'] = Header(strSubject, 'utf-8')
        message['From'] = Header(strSendAddr, 'utf-8')
        message['To'] = Header(str(listToAddr), 'utf-8')
        if CCToAddr != None:
            message['Cc'] = Header(str(CCToAddr), 'utf-8')

        message.attach(MIMEText(strContent, 'plain', 'utf-8'))

        annexFile = MIMEText(
            open(
                strErrFilePath,
                'rb').read(),
            'base64',
            'utf-8')
        annexFile["Content-Type"] = 'application/octet-stream'
        annexFile["Content-Disposition"] = (('attachment; filename="%s"') %filename)
        message.attach(annexFile)

        try:
            smtpObj = SMTP_SSL(strSmtpServer)
            smtpObj.set_debuglevel(1)
            smtpObj.ehlo(strSmtpServer)
            smtpObj.login(strSendAddr, strPasswd)
            print("登陆成功", 'runLog')
            if(CCToAddr != None and listToAddr != None) :
                print("接受地址不为空")
                print(listToAddr)
                print(CCToAddr)
                print(listToAddr.split(",") + CCToAddr.split(","))
                smtpObj.sendmail(strSendAddr, listToAddr.split(",") + CCToAddr.split(","), message.as_string())
                smtpObj.quit()
            elif(CCToAddr == None and listToAddr != None) :
                print("接受地址不为空")
                print(listToAddr)
                print(CCToAddr)
                smtpObj.sendmail(strSendAddr, listToAddr, message.as_string())
                smtpObj.quit()
            else:
                print("接受邮件地址为空")
                print("附件邮件发送成功")
        except BaseException:
            print(sys.exc_info()[0])
            print("附件邮件发送失败")
