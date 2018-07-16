#!user/bin/env python
# coding=utf-8
# @Author  : Dang
# @Time    : 2018/5/22 17:25
# @Email   : 1370465454@qq.com
# @File    : 
# @Description:爬去酒店信息


from bs4 import BeautifulSoup
import requests
import time
import re

url='http://search.qyer.com/hotel/89580_4.html'
urls=['http://search.qyer.com/hotel/89580_{}.html'.format(str(i)) for i in range(1,10)] # 最多157页
# print(urls)
infos=[]


def get_url(urls):
    '''批量爬取数据'''
    data_number=0
    for url in urls:
        getAttractions(url)
        print('-----{}------'.format(len(infos)),sep='\n')


def getAttractions(url,data=None):
    '''爬取当前页面数据'''
    web_data=requests.get(url)
    time.sleep(2)
    soup=BeautifulSoup(web_data.text,'lxml')#lxml HTML 解析器BeautifulSoup(markup, “lxml”)
    # print(soup)
    hotel_names=soup.select('ul.shHotelList.clearfix > li > h2 > a')
    hotel_images=soup.select('span[class="pic"] > a > img')
    hotel_points = soup.select('span[class="points"]')
    hotel_introduces = soup.select('p[class="comment"]')
    hotel_prices = soup.select('p[class="seemore"] > span > em')

    if data==None:
        for name,image,point,introduce,price in zip(hotel_names,hotel_images,hotel_points,hotel_introduces,hotel_prices):
            data={
                'name':name.get_text().replace('\r\n','').strip(),
                'image':image.get('src'),
                'point':re.findall(r'-?\d+\.?\d*e?-?\d*?', point.get_text())[0],
                'introduce':introduce.get_text().replace('\r\n','').strip(),
                'price':int(price.get_text())
            }

            infos.append(data)
# 根据价格从高到低进行排序
def getInfosByPrice(infos = infos):
    infos = sorted(infos, key=lambda info: info['price'], reverse=True)
    for info in infos:
        print(info['price'], info['name'])
get_url(urls)
getInfosByPrice(infos)