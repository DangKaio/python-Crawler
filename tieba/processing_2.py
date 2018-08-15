#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Dang Kai
# @Date: 2018-08-08 15:31:14
# @Last Modified time: 2018-08-15 09:32:19
# @E-mail: 1370465454@qq.com
# @Description: 进程池
from multiprocessing import Pool
import os,time,random
#启动大量的子进程，可以用进程池批量创建子进程
def long_time_task(name):
    print('运行任务 %s (%s)' % (name,os.getpid()))
    start=time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('任务 %s 运行 %0.2f seconds. ' % (name,(end-start)))
if __name__ == '__main__':
    print('主进程 %s。' % os.getpid())
    p=Pool(4)
    for i in range(5):
        p.apply_async(long_time_task,args=(i,))
    print('等待所有进程执行')
    p.close()
    p.join()
    print('执行完成')