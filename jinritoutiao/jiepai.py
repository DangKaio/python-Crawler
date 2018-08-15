#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Dang Kai
# @Date: 2018-08-15 09:15:55
# @Last Modified time: 2018-08-15 16:39:40
# @E-mail: 1370465454@qq.com
# @Description: 今日头条ajax 请求
import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import json
import os
from hashlib import md5
from json import JSONDecodeError
import re
from urllib.parse import urlencode
from multiprocessing import Pool


GROUP_START=1
GROUP_END=2

KEYWORD='街拍'
def get_page_index(offset,keyword):     #请求首页页面html
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'search_tab'
    }
    url ='https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except Exception:
        print('请求首页出错')
        return None

def parse_page_index(html):         #解析首页获得的html
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detalil(url):          #请求详情页面html
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except Exception:
        print('请求详情页出错',url)
        return None

def parse_page_detail(html,url):        #解析每个详情页内容
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    image_pattern = re.compile('gallery: JSON.parse\("(.*)"\)',re.S)
    result = re.search(image_pattern,html)
    if result:
        try:
            data = json.loads(result.group(1).replace('\\',''))
            if data and 'sub_images' in data.keys():
                sub_images = data.get("sub_images")
                images = [item.get('url') for item in sub_images]
                for image in images:download_image(image)
                return {
                    'title':title,
                    'url':url,
                    'images':images
                }
        except JSONDecodeError:
            pass
def download_image(url):        #查看图片链接是否正常获取
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    print('正在下载：',url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        print('请求图片出错', url)
        return None

def save_image(content):        #下载图片到指定位置

    #file_path = '{}/{}.{}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    file_path = '{}/{}.{}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html = get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detalil(url)
        if html:
            result = parse_page_detail(html,url)

if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()

    pool.map(main,groups)