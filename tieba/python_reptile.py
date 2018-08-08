#!user/bin/env python
# coding=utf-8
# @Author  : Dang
# @Time    : 2018/5/22 17:25
# @Email   : 1370465454@qq.com
# @File    : 
# @Description:爬去贴吧图片

from urllib import request
import re
import os

def get_Html(url):
    '''获取网页源码'''
    page=request.urlopen(url)
    htmlcode=page.read()#读取页面源码
    # print(htmlcode.decode("UTF-8"))
    return htmlcode.decode("UTF-8")


def get_Img(html):
    reg=r'src="(.+?\.jpg)" pic_ext'#https://imgsa.baidu.com/forum/w%3D580/sign=294db374d462853592e0d229a0ee76f2/e732c895d143ad4b630e8f4683025aafa40f0611.jpg
    imgre=re.compile(reg)
    imglist=re.findall(imgre, html)
    path = os.getcwd()+'\\test'
    # 将图片保存到D:\\test文件夹中，如果没有test文件夹则创建
    if not os.path.isdir(path): 
        os.makedirs(path)  
    paths = path+'\\'      #保存在test  下
    imgName=0
    for imgPath in imglist:
        request.urlretrieve(imgPath,'{}{}.jpg'.format(paths,imgName))
        imgName+=1
    print('总共%s张照片' % imgName)
if __name__ == '__main__':
    html = get_Html("http://tieba.baidu.com/p/2460150866")#获取该网址网页详细信息，得到的html就是网页的源代码  
    get_Img(html) #从网页源代码中分析并下载保存图片   [Finished in 6.2s]