# -*- coding: utf-8 -*-
# @Time : 2018/8/3 17:29
# @Author : sunlin
# @File : timer.py
# @Software: PyCharm
import threading
import datetime
import schedule
from model.FUNC.configure import getConfig




def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def job2():
    print("I'm working for job2")
    print("job2:", datetime.datetime.now())
    print('------------------------')


def job1_task():
    threading.Thread(target=job2).start()




class Timer:
    def run_task(self):
        try:
            mode = getConfig('TIMING_TIME', 'mode')
            t = getConfig('TIMING_TIME', 'time')
            int_t = int(t)
            if mode == 'minutes':
                schedule.every(int_t).minutes.do(job1_task)
            elif mode == 'hour':
                schedule.every().hour.do(job1_task)
            while True:
                schedule.run_pending()
        except Exception as e:
            print(e)

    def run(self):
        pass


if __name__ == '__main__':
    Timer().run_task()
