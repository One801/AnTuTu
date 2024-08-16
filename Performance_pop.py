# 参考网站：https://www.cnblogs.com/cdwyyds/p/14915228.html
import requests
from bs4 import BeautifulSoup
import time
import random
import sys
import re
from tqdm import tqdm
from lxml import etree
import xml.etree.ElementTree as ET

# 随机头

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER"
]
headers = {
    'User-Agent': random.choice(USER_AGENTS),
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
}

# url = 'http://www.antutu.com/ranking/rank1.htm'
url = 'https://www.antutu.com/ranking/ios.htm'


# file = open("data/AndroidPhone_pop.csv", "a")

def Antutu():
    ress = requests.get(url, headers=headers)
    ress.encoding = 'utf-8'

    html = etree.HTML(ress.text)
    # print(html)
    # 初始化查询数据
    a = 3
    phone_mem_coun = 4
    phone_ux_coun = 5
    phone_sum_coun = 6
    phone_gpu_coun = 3
    # 分析手机排行榜信息：手机名称name、手机cpu分数phone_cpu、手机gpu分数phone_gpu、Mem分数phone_me、UX分数phone_ux、总分phone_sum
    for i in range(3, 43):
        name = html.xpath("//*[@id='rank']/div[1]/div/div/div[1]/div/div[1]/div/ul[{}]/a/div[2]/li[1]/text()".format(a))
        phone_cpu = html.xpath(
            "//*[@id='rank']/div[1]/div/div/div[1]/div/div[1]/div/ul[{}]/a/div[2]/li[2]/text()".format(a))
        phone_gpu = html.xpath(
            "//*[@id='rank']/div[1]/div/div/div[1]/div/div[1]/div/ul[{}]/a/div[2]/li[{}]/text()".format(a,
                                                                                                        phone_gpu_coun))
        phone_mem = html.xpath(
            "//*[@id='rank']/div[1]/div/div/div[1]/div/div[1]/div/ul[{}]/a/div[2]/li[{}]/text()".format(a,
                                                                                                        phone_mem_coun))
        phone_ux = html.xpath(
            "//*[@id='rank']/div[1]/div/div/div[1]/div/div[1]/div/ul[{}]/a/div[2]/li[{}]/text()".format(a,
                                                                                                        phone_ux_coun))
        phone_sum = html.xpath(
            "//*[@id='rank']/div[1]/div/div/div[1]/div/div[1]/div/ul[{}]/a/div[2]/li[{}]/text()".format(a,
                                                                                                        phone_sum_coun))

        a += 1
        sum = name + phone_cpu + phone_gpu + phone_mem + phone_ux + phone_sum
        print(sum)
        # with open('data/AndroidPhone_pop.csv', "a", encoding='utf-8') as file1:
        with open('data/IosPhone_pop.csv', "a", encoding='utf-8') as file1:
            if file1.tell() == 0:  # 检查文件的第一行是否为空
                file1.write(
                    "name" + "," + "phone_cpu" + "," + "phone_gpu" + "," + "phone_mem" + "," + "phone_ux" + "," + "phone_sum" + "\n")
            else:
                file1.write(sum[0] + "," + sum[1] + "," + sum[2] + "," + sum[3] + "," + sum[4] + "," + sum[5] + "\n")


if __name__ == '__main__':
    Antutu()
