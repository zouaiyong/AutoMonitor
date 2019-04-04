# -*- coding: utf-8 -*-
# @Time : 2018/8/6 16:33
# @Author : sunlin
# @File : dfs.py
# @Software: PyCharm
import datetime
import schedule
import time

from model.util.operate import Operate


def job1():
    print("I'm working for job1")
    time.sleep(2)
    print("job1:", datetime.datetime.now())


def job2():
    print("I'm working for job2")
    time.sleep(2)
    print("job2:", datetime.datetime.now())


def run():
    schedule.every(10).seconds.do(job1)
    schedule.every(10).seconds.do(job2)

    while True:
        schedule.run_pending()
        time.sleep(1)

run()
Operate()