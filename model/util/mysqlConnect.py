# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 10:12
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : mysqlConnect.py
# @Software: PyCharm

import pymysql.cursors

class DoMysql(object):

    # 连接数据库,返回一条连接
    
    def __init__(self, dictMsgForMysql):

        # 构造函数

        self.strHost = dictMsgForMysql.get('host')
        self.strPort = dictMsgForMysql.get('port')
        self.strUser = dictMsgForMysql.get('user')
        self.strPasswd = dictMsgForMysql.get('passwd')
        self.strDatabase = dictMsgForMysql.get('database')
        self.charset=dictMsgForMysql.get('charset')
        print('host=%s port=%s user=%s passwd=%s database=%s' %(self.strHost,self.strPort,self.strUser,self.strPasswd,self.strDatabase))

    def connectionMySQL(self):

        # 连接数据库
        # 返回一个连接

        connection = None

        try:
            connection = pymysql.connect(host = self.strHost, port = int(self.strPort), user = self.strUser,
                                     passwd = self.strPasswd, db = self.strDatabase,
                                     charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print(e)
            print('请重新检查数据库配置(可能配置出错或者网络出错)')
        return connection

class getJsonMysql:
    # 获取数据库连接
    def getConJson(self,dictMsgForMysql):
        return DoMysql(dictMsgForMysql).connectionMySQL()

    # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典
    def exeQueryJson(self, sql,dictMsgForMysql):
        conn = self.getConJson(dictMsgForMysql)
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cur.execute(sql)
            # exeLog("====执行成功====SQL语句：" + str(sql))
            # fco = cur.fetchall()
            return cur
        except Exception as e:
            print("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            conn.close()

    def get_JSON(self,sql,dictMsgForMysql):
        db = getJsonMysql()
        a = db.exeQueryJson(sql,dictMsgForMysql)
        # 默认获取查询的所有数据
        b = a.fetchall()
        if b == ():
            # exeLog("====查询结果为空====SQL语句：" + str(sql))
            return False

        else:
            # exeLog("====查询成功====SQL语句：" + str(sql))
            return b


if __name__ == "__main__":
    host = "10.100.99.7"
    port = "3306"
    user = "admin"
    passwd = "password"
    database = "tmp_v3"
    charset = "utf8"
    dictMsgForMysql = {"host":host,"port":port,"passwd":passwd,"user":user,"database":database,"charset":charset}
    sql = "select * from p_env_email_confg WHERE email_id = '{}'".format("41628")
    A = getJsonMysql().get_JSON(sql,dictMsgForMysql)
    print(A)