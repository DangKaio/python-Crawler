#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Dang Kai
# @Date: 2018-08-08 16:30:10
# @Last Modified time: 2018-08-08 17:03:25
# @E-mail: 1370465454@qq.com
# @Description: 进程间通信 python 的multiprocessing提供了queue 、Pipes等多种方式来交换数据

from multiprocessing import Process, Queue
import os
import time
import random

# 用于写入数据进程


def write(data):
    print('此进程用于写入：%s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('写入%s 到队列' % value)
        data.put(value)
        time.sleep(random.random())
# 用于读取数据的进程


def read(data):
    print('此进程用于读取：%s' % os.getpid())
    while True:
        value = data.get(True)
        print('获取数据%s 从队列' % value)
        pass


if __name__ == '__main__':
    #父进程创建Queue
    m_queue=Queue()
    pw=Process(target=write,args=(m_queue,))
    pr=Process(target=read,args=(m_queue,))
    #启动子进程pw 写入
    pw.start()
    #启动子进程pr 读取
    pr.start()
    #等待pw 结束
    pw.join()
    #pr进程里是死循环，无法等待其结束，则 强制
    pr.terminate()

#此处有个问题 必须在cmd下运行才会执行read ，在sublime运行不了网上说是解释器问题