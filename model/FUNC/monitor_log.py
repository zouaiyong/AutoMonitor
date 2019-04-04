# -*- coding: utf-8 -*-
# @Time : 2018/8/7 10:34
# @Author : sunlin
# @File : monitor_log.py
# @Software: PyCharm
import datetime
import os
import time
from model.FUNC.configure import getConfig


dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_filename = "TEST-" + time.strftime(r'%Y-%m-%d', time.localtime(time.time())) + ".log"
log_path = dir + os.sep + 'log' + os.sep + log_filename


def monitor_log():
    word = getConfig('MONITOR_LOG', 'keyword')
    list_xin = []
    with open(log_path, 'r', encoding='UTF-8') as f:
        for i in f:
            if word in i:
                list_xin.append(i)
    print(list_xin, datetime.datetime.now())
    return str(list_xin)


if __name__ == '__main__':
    print(monitor_log())