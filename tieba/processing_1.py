#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Dang Kai
# @Date: 2018-08-08 15:05:56
# @Last Modified time: 2018-08-08 15:30:56
# @E-mail: 1370465454@qq.com
# @Description:
from multiprocessing import Process
import os


def run_proc(name):
    print('运行子进程 %s (%s)' % (name, os.getpid()))
    i = 0
    print(i)
if __name__ == '__main__':
    print('主进程 %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('子进程将启动')
    p.start()
    p.join()#join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    print('子进程结束')
