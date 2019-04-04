#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 14:04
# @Author  : kimmy-pan
# @File    : getEmailInfo.py
from model.util.mysqlConnect import *
import configparser
import os



def getConfig(session,key):
    config=configparser.ConfigParser(
        allow_no_value=True, delimiters='=')
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\util\\config.ini'
    config.read(path)
    return config.get(session,key)


def get_from_db():
    list = []
    host = getConfig("GETEMAIL_DATABASE", "host")
    port = getConfig("GETEMAIL_DATABASE", "port")
    user = getConfig("GETEMAIL_DATABASE", "user")
    passwd = getConfig("GETEMAIL_DATABASE", "passwd")
    database = getConfig("GETEMAIL_DATABASE", "database")
    charset = getConfig("GETEMAIL_DATABASE", "charset")

    dictMsgForMysql = {"host":host,"port":port,"passwd":passwd,"user":user,"database":database,"charset":charset}
    sql = "SELECT warning_email_id FROM `w_warning_info`"
    result = getJsonMysql().get_JSON(sql, dictMsgForMysql)
    if result != False:
        for i in eval(result[0]["warning_email_id"]):
            sql_config = "select * from p_env_email_confg WHERE email_id = '{}'".format(i)
            result_config = getJsonMysql().get_JSON(sql_config,dictMsgForMysql)
            if result_config != False:
                list.append(result_config[0])
    return list
    # for i in email_id:
    #     sql = "select * from p_env_email_confg WHERE email_id = '{}'".format(i)
    #     result = getJsonMysql().get_JSON(sql,dictMsgForMysql)
    #     if result != False:
    #         list.append(result[0])
    # return list


def Email_Info():
    emailInfo = {}
    all_emailInfo = []
    result = get_from_db()
    for i in result:
        emailInfo["email_sendaddr"] = i["email_sender"]
        emailInfo["email_sendpasswd"] = i["email_password"]
        emailInfo["smtp_server"] = "smtp.exmail.qq.com"
        emailInfo["ToEmail"] = i["email_mainrecv"].replace(";",",")
        emailInfo["CcEmail"] = i["email_cc"].replace(";",",")
        emailInfo["email"] = "yes"
        all_emailInfo.append(str(emailInfo))
    # emailInfo["email_sendaddr"] = result["email_sender"]
    # emailInfo["email_sendpasswd"] = result["email_password"]
    # emailInfo["smtp_server"] = "smtp.exmail.qq.com"
    # emailInfo["ToEmail"] = result["email_mainrecv"].replace(";", ",")
    # emailInfo["CcEmail"] = result["email_cc"].replace(";", ",")
    # emailInfo["email"] = "yes"
    return all_emailInfo


if __name__ == "__main__":
    print(Email_Info()[0])