# -*- coding: utf-8 -*-
# @Time : 2018/8/6 15:20
# @Author : sunlin
# @File : configure.py
# @Software: PyCharm
import configparser
import os


def getConfig(section, key):
    dir_work = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = dir_work + os.sep + 'util' + os.sep + 'config.ini'
    config_obj = configparser.ConfigParser(allow_no_value=True)
    config_obj.read(config_path)
    value = config_obj.get(section, key)
    return value


if __name__ == '__main__':
    print(getConfig('TIMING_TIME', 'mode'))
