# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 15:12
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : dbCheck.py
# @Software: PyCharm
import configparser
import datetime
import os
from model.util.mysqlConnect import *

from model.FUNC.dataTemplate import DataTemplate
from model.FUNC.prettyTableDo import PrettyTableDo

from model.util.mysqlConnect import DoMysql
from model.util.sysTime import RunTime


class SqlCheck():
    def __init__(self, dictRunmsg, dataTemplateObj):
        self.dataTemplate = dataTemplateObj
        self.runTime = RunTime()
        if isinstance(dictRunmsg, dict):
            if dictRunmsg.get('check_time'):
                self.checktime = dictRunmsg.get('check_time')
            else:
                self.checktime = datetime.date.today()
            print('check_time=',self.checktime)
            dictMsgForCheckLetter = self.getMsgForCheckLetter(dictRunmsg)
            dictMsgForMysql = self.getMsgForMysql(dictRunmsg)

            if (((len(dictMsgForCheckLetter) == 1) and ('err' in dictMsgForCheckLetter)) or
                    ((len(dictMsgForMysql) == 1) and ('err' in dictMsgForMysql))):
                print("检测数据库字段所需配置不全, 致检测任务中止运行", 'runLog')
            else:
                self.host = dictRunmsg.get('host')
                self.port = dictRunmsg.get('port')
                self.user = dictRunmsg.get('user')
                self.passwd = dictRunmsg.get('passwd')
                self.database = dictRunmsg.get('database')
                self.table_name = dictRunmsg.get('table_name')
                self.field_name = dictRunmsg.get('field_name')
                self.field_name_time = dictRunmsg.get('field_name_time')
                self.fieldcompare_value = dictRunmsg.get('fieldcompare_value')
                self.checkRun(dictMsgForMysql)

    def getMsgForMysql(self, dictNeedRunMsg):
        # 获取连接mysql数据库所需要的数据，并判断是否完全
        # 返回一个dict类型的数据
        # 存放的字段
        # host
        # port
        # user
        # passwd
        # database

        dictMsgForMysql = {}

        for keyItem in dictNeedRunMsg:
            if ((keyItem == 'host') | (keyItem == 'port') | (keyItem == 'user') | (
                    keyItem == 'passwd') | (keyItem == 'database')):
                if (dictNeedRunMsg.get(keyItem) != ''):

                    dictMsgForMysql[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForMysql.clear()
                    dictMsgForMysql['err'] = "Msg Incomplete"
                    break

        return dictMsgForMysql

    def getMsgForCheckLetter(self, dictNeedRunMsg):

        # 获取检测数据库字段所需的数据，并判断是否完全
        # 返回一个dict类型的数据
        # 存放的字段有
        # table_name
        # field_name
        # field_name_time
        # fieldcompare_value
        dictMsgForCheckLetter = {}

        for keyItem in dictNeedRunMsg:
            if ((keyItem == 'table_name') | (keyItem == 'field_name') | (
                    keyItem == 'field_name_time') | (keyItem == 'fieldcompare_value')):
                if (dictNeedRunMsg.get(keyItem) != ''):

                    dictMsgForCheckLetter[keyItem] = dictNeedRunMsg.get(
                        keyItem)
                else:
                    dictMsgForCheckLetter.clear()
                    dictMsgForCheckLetter['err'] = "Msg Incomplete"
                    break

        return dictMsgForCheckLetter

    def checkRun(self, dictMsgForMysql):
        doMySql = DoMysql(dictMsgForMysql)
        objConnection = doMySql.connectionMySQL()
        self.findTheField(objConnection)

    def findTheField(self, objConnection):
        # 查找设定表中的设定字段的值
        # objConnection: 数据库的一条连接
        # table_name: 表名
        # field_name: 字段名
        # fieldcompare_value: 字段名的值
        # 获取之后将其返回，类型为list集合

        listResult = []

        if objConnection is None:
            print("数据库连接失败")
        else:
            print("数据库连接成功")
            print(("准备查找%s表中%s字段值为%s的数据") %
                  (self.table_name ,self.field_name,self.fieldcompare_value))
            try:
                with objConnection.cursor() as cursor:
                    strSearchSql = (
                        "SELECT " +
                        " *" +
                        " FROM " +
                        self.table_name +
                        " WHERE " +
                        self.field_name +
                        "= %s AND " +
                        self.field_name_time +
                        " >= '%s'")
                    print(strSearchSql %
                          (self.fieldcompare_value, self.checktime))
                    cursor.execute(
                        strSearchSql %
                        (self.fieldcompare_value, self.checktime))

                    listResult = cursor.fetchall()
                    cursor.close()
                    if (listResult is None) or (len(listResult) == 0):
                        print(
                            (("未查找到%s表中%s字段值为%s的数据") %
                             (self.table_name,self.field_name,self.fieldcompare_value)))
                    else:

                        strValueMsgTable = PrettyTableDo().getMsgForTableShowByListDict(listResult, 1)
                        print(("已监控到%d条数据,如下" % (len(listResult))))
                        print(strValueMsgTable)
                        strLogContent = ((self.database + "数据库中,  " + "有" + str(len(listResult)) + "条记录，字段" + self.field_name +
                                              "的值是%s的") % (self.fieldcompare_value))
                        self.dataTemplate.detailAll = (('<h2>监控到%s 如下：</h2><br/>' + strValueMsgTable) %(strLogContent))
                        self.dataTemplate.dataAll=strLogContent
            finally:
                if objConnection._closed:
                    print("第一次查询连接意外关闭")
                else:
                    objConnection.close()
                    print("第一次查询连接已正常关闭")

    pass


def readConfigureFile():
        # 读取脚本配置文件
        # print("readConfigureFile读取配置文件")
    dictConfMsgTotal = {}
    dictConfMsg = {}
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('dir=', dir)
    configureFileNameAndPath = dir + os.sep + 'util' + os.sep + 'config.ini'
    configParserObj = configparser.ConfigParser(
        allow_no_value=True, delimiters='=')
    configParserObj.read(configureFileNameAndPath)
    try:
        listSectionName = configParserObj.sections()
    except BaseException:
        print("读取配置文件出错")

    else:
        for sectionItem in listSectionName:
            if (sectionItem == 'CHECK_DATABASE')| (
                    sectionItem == 'CHECK_TABLE')|(sectionItem=='Dingtalk')|(sectionItem=='ToEmail')|(sectionItem=='EmailConfigure')|(sectionItem=='CHECK_TIME'):
                listKeyName = configParserObj.options(sectionItem)
                print(listKeyName)
                sectionObj = configParserObj[sectionItem]
                if (len(listKeyName) != 0):
                    for keyItem in listKeyName:
                        valueItem = sectionObj[keyItem]
                        if (valueItem is None):
                            dictConfMsg[sectionItem] = listKeyName
                        else:
                            dictConfMsg[keyItem] = valueItem
                else:
                    dictConfMsg[sectionItem] = ''
        # print(dictConfMsg)
    dictConfMsgTotal.update(dictConfMsg)
    # print("dictConfMsgTotal如下")
    # print(dictConfMsgTotal)
    if (len(dictConfMsgTotal) == 0):
        print("未获取到配置文件内容")
    else:
        print("读取到的配置文件信息如下: ")
        print(str(dictConfMsgTotal))
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(dictConfMsgTotal)
    return dictConfMsgTotal


def Get_DB_Keyword(task_id,dataTemplateObj):
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('dir=', dir)
    configureFileNameAndPath = dir + os.sep + 'util' + os.sep + 'config.ini'
    configParserObj = configparser.ConfigParser(
        allow_no_value=True, delimiters='=')
    configParserObj.read(configureFileNameAndPath)
    host = configParserObj.get("GETEMAIL_DATABASE", "host")
    port = configParserObj.get("GETEMAIL_DATABASE", "port")
    user = configParserObj.get("GETEMAIL_DATABASE", "user")
    passwd = configParserObj.get("GETEMAIL_DATABASE", "passwd")
    database = configParserObj.get("GETEMAIL_DATABASE", "database")
    charset = configParserObj.get("GETEMAIL_DATABASE", "charset")
    dictMsgForMysql = {"host": host, "port": port, "passwd": passwd, "user": user, "database": database,
                       "charset": charset}
    caselevel_sql = "SELECT warning_info FROM `w_warning_info`"
    get_caselevel = str(eval(getJsonMysql().get_JSON(caselevel_sql, dictMsgForMysql)[0]["warning_info"])["case_type"])
    sql = "SELECT t.task_id,c.case_result,d.case_level FROM t_task_to_case t INNER JOIN ((SELECT *,'core' AS case_table FROM core_case_result) UNION ALL (SELECT *,'regress' AS case_table FROM regress_case_result)) c ON c.case_id=t.case_id  LEFT JOIN ((SELECT *,'core' AS case_table FROM core_case_info) UNION ALL (SELECT *,'regress' AS case_table FROM regress_case_info)) d ON d.case_id=c.case_id    WHERE" \
          " t.task_id='{}' and case_level in ({}) and case_result != 1".format(task_id,get_caselevel.replace("[","").replace("]",""))
    result = getJsonMysql().get_JSON(sql, dictMsgForMysql)
    # RECORD BY [panshuhua]: case_result != 1都告警
    if result !=False:
        print(result)
        strValueMsgTable = PrettyTableDo().getMsgForTableShowByListDict(result, 1)
        print(("已监控到%d条数据,如下" % (len(result))))
        print(strValueMsgTable)
        strLogContent = ((task_id + "：" + "有" + str(len(result)) + "条数据，case_result!=1"))
        dataTemplateObj.detailAll = (('<h2>监控到%s 如下：</h2><br/>' + strValueMsgTable) % (strLogContent))
        dataTemplateObj.dataAll = strLogContent

    else:
        print(
            (("未查找到case_result!=1数据") ))


if __name__ == '__main__':
    dictMsgRun = readConfigureFile()
    print(dictMsgRun)
    dataTemplateObj = DataTemplate(
         RunTime().getDateTime())
    print(dictMsgRun.get('ToEmail'))
    checksql = SqlCheck(dictMsgRun, dataTemplateObj)
