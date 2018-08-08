#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Dang Kai
# @Date: 2018-08-08 15:21:28
# @Last Modified time: 2018-08-08 16:29:18
# @E-mail: 1370465454@qq.com
# @Description:
from urllib import request
import re
import os
import random
import time
from multiprocessing import Pool


def get_Html(url):
    '''获取网页源码'''
    page = request.urlopen(url)
    htmlcode = page.read()  # 读取页面源码
    # print(htmlcode.decode("UTF-8"))
    return htmlcode.decode("UTF-8")


def get_Img_url(html):
    # https://imgsa.baidu.com/forum/w%3D580/sign=294db374d462853592e0d229a0ee76f2/e732c895d143ad4b630e8f4683025aafa40f0611.jpg
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    return imglist


def download_path():
    path = os.getcwd() + '\\test'
    # 将图片保存到D:\\test文件夹中，如果没有test文件夹则创建
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path + '\\'  # 保存在test  下
    return paths


def run_func(imgCount, url):
    print('运行子进程 %s (%s)' % (imgCount, os.getpid()))
    paths = download_path()
    print('down %s' % url)
    request.urlretrieve(url, '{}{}.jpg'.format(paths, imgCount))


def long_time_task(name):
    '''测试使用'''
    print('运行任务 %s (%s)' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('任务 %s 运行 %0.2f seconds. ' % (name, (end - start)))

    
if __name__ == '__main__':
    print('主进程 %s.' % os.getpid())
    # 获取该网址网页详细信息，得到的html就是网页的源代码
    html = get_Html("http://tieba.baidu.com/p/2460150866")
    imglist = get_Img_url(html)  # 从网页源代码中分析并下载保存图片   [Finished in 6.2s]
    p = Pool(4)
    for imgCount in range(len(imglist)):
        p.apply_async(run_func, args=(imgCount, imglist[imgCount]))
    print('等待所有进程执行')
    p.close()
    p.join()
    print('执行完成')
