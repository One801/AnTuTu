import csv
import os.path
import urllib

import requests
import re
import json
from bs4 import BeautifulSoup
import webbrowser
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import concurrent.futures

urls = ['https://www.antutu.com/ranking/rank1.htm',
        'https://www.antutu.com/ranking/rank2.htm',
        'https://www.antutu.com/ranking/judge.htm',
        'https://www.antutu.com/ranking/ios.htm',
        'https://www.antutu.com/ranking/judgeios.htm'
]

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
for url in urls:
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    be = BeautifulSoup(r.text, features="lxml")
    if requests.status_codes==200:
        C = be.select('ul[class="list-unstyled newrank-b"] a')
        name = be.select('ul[class="list-unstyled newrank-b"] a div li[class="bfirst"]')#性能'''
    else:
        C = be.select('ul[class="list-unstyled newrankxjb newrankxjb-b"] a')
        name = be.select('ul[class="list-unstyled newrankxjb newrankxjb-b"] a div li[class="newrankc"]')  # 性价比，好评

    print(url)
for a in range(3, 5):
    # phonename = re.findall(r'</span>(.*?)<span', str(name[a]), re.S)
    phonename = re.findall(r'</span>(.*?)</li', str(name[a]), re.S)  # 好评
    # 手机名称
    # print(phonename)
    rankhref = C[a].get('href')
    a = a + 1
    # print(mobilehref)
    url1 = rankhref
    # webbrowser.get('chrome').open(url1,new=1,autoraise=True)
    cookies = [{'domain': 'www.jd.com', 'expiry': 1697766707, 'httpOnly': False, 'name': 'UseCorpPin', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'},
               {'domain': '.jd.com', 'expiry': 1732323107, 'httpOnly': False, 'name': 'shshshfpb', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': 'AAjQnkUqLEoFE_zF40NVjMmnYcI9qrxaXdjBXQAAAAAA'},
               {'domain': '.jd.com', 'expiry': 1697764906, 'httpOnly': False, 'name': '__jdb', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '76161171.3.16977630565491836939262|1.1697763057'},
               {'domain': '.jd.com', 'expiry': 1713315106, 'httpOnly': False, 'name': '__jda', 'path': '/',
                'sameSite': 'Lax', 'secure': False,
                'value': '76161171.16977630565491836939262.1697763057.1697763057.1697763057.1'},
               {'domain': '.jd.com', 'expiry': 1700355103, 'httpOnly': False, 'name': 'unick', 'path': '/',
                'sameSite': 'None', 'secure': True, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'},
               {'domain': 'www.jd.com', 'expiry': 1729299057, 'httpOnly': False, 'name': 'o2State', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '{%22webp%22:true%2C%22avif%22:true}'},
               {'domain': '.jd.com', 'expiry': 1723683103, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/',
                'sameSite': 'Lax', 'secure': False,
                'value': 'K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQ'},
               {'domain': '.jd.com', 'expiry': 1700355103, 'httpOnly': False, 'name': 'pin', 'path': '/',
                'sameSite': 'None', 'secure': True, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'},
               {'domain': '.jd.com', 'expiry': 1697764907, 'httpOnly': False, 'name': 'shshshsID', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '9e55c25c56587f69286b3af9301867e0_2_1697763107372'},
               {'domain': '.jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'sameSite': 'Lax',
                'secure': False, 'value': '76161171'},
               {'domain': '.jd.com', 'expiry': 1729299103, 'httpOnly': False, 'name': 'pinId', 'path': '/',
                'sameSite': 'None', 'secure': True, 'value': '9AtnzikIiXEpN177ctDmyg'},
               {'domain': '.jd.com', 'expiry': 1728867057, 'httpOnly': False, 'name': '3AB9D23F7A4B3CSS', 'path': '/',
                'sameSite': 'Lax', 'secure': False,
                'value': 'jdd03K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQAAAAMLJKIGFCYAAAAACXVHT47AXCRXX4X'},
               {'domain': '.jd.com', 'expiry': 1698367857, 'httpOnly': False, 'name': 'PCSYCityID', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': 'CN_430000_431300_0'},
               {'domain': '.jd.com', 'expiry': 1700355103, 'httpOnly': True, 'name': '_pst', 'path': '/',
                'sameSite': 'None', 'secure': True, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'},
               {'domain': '.jd.com', 'expiry': 1698627057, 'httpOnly': False, 'name': 'ipLoc-djd', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '18-1586-0-0'},
               {'domain': '.jd.com', 'expiry': 1699059056, 'httpOnly': False, 'name': '__jdv', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '76161171|direct|-|none|-|1697763056549'},
               {'domain': '.jd.com', 'expiry': 1732323107, 'httpOnly': False, 'name': 'shshshfpx', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '568144ff-3178-d0d5-6332-69d8708f6aaf-1697763057'},
               {'domain': '.jd.com', 'expiry': 1732323107, 'httpOnly': False, 'name': 'shshshfpa', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '568144ff-3178-d0d5-6332-69d8708f6aaf-1697763057'},
               {'domain': '.jd.com', 'expiry': 1698367903, 'httpOnly': True, 'name': 'flash', 'path': '/',
                'sameSite': 'None', 'secure': True,
                'value': '2_6mErC-376A88YnJOYHdB2imkHYi54LJrcwQIKAopilUg0VpzXSN_O1GHEVyUnTCsdQ-TzKiSJXYxOAnIwTiJ_wrATmPmU4Zq1sy_9R1keNq*'},
               {'domain': '.jd.com', 'expiry': 1698627057, 'httpOnly': False, 'name': 'areaId', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '18'},
               {'domain': '.jd.com', 'expiry': 1698367903, 'httpOnly': True, 'name': 'thor', 'path': '/',
                'sameSite': 'None', 'secure': True,
                'value': '7B4AFE61F6A4E8F7376A98CEF1F990908F76390130E167B712E3F0262E51AC16D982221E9BBCBC6EF8051F7936772C70568155CA24291BDAB844247FA0301AC5F3C6F459A1817C39125BEA62A210BB4A40E8944B8DC6056D496095708D4289C9F848090C2EC75559D5C17CDDB7E1779988275E7A32EB458B449A470B2C0BB064'},
               {'domain': '.jd.com', 'expiry': 1700355103, 'httpOnly': False, 'name': '_tp', 'path': '/',
                'sameSite': 'None', 'secure': True, 'value': 'ilfzk4qmKQELFG9iaEwJF0ePLXlTTRyu9Ntm%2FIwkHDo%3D'},
               {'domain': '.jd.com', 'httpOnly': False, 'name': 'ceshi3.com', 'path': '/', 'sameSite': 'None',
                'secure': True, 'value': '000'},
               {'domain': '.jd.com', 'expiry': 1697763177, 'httpOnly': False, 'name': '_gia_d', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '1'},
               {'domain': '.jd.com', 'expiry': 1713315108, 'httpOnly': False, 'name': '__jdu', 'path': '/',
                'sameSite': 'Lax', 'secure': False, 'value': '16977630565491836939262'}]
    '''cookies2=[{'domain': 'www.jd.com', 'expiry': 1697820944, 'httpOnly': False, 'name': 'UseCorpPin', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'jd_liPodPFvasNd'}, {'domain': '.jd.com', 'expiry': 1732377344, 'httpOnly': False, 'name': 'shshshfpb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'AAki4zE2LEnIBImO96wDJKtDpkXgRvRaXgXMGQAAAAAA'}, {'domain': '.jd.com', 'expiry': 1697819142, 'httpOnly': False, 'name': '__jdb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171.3.16978173043551234917588|1.1697817304'}, {'domain': '.jd.com', 'expiry': 1713369342, 'httpOnly': False, 'name': '__jda', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171.16978173043551234917588.1697817304.1697817304.1697817304.1'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': False, 'name': 'unick', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'jd_liPodPFvasNd'}, {'domain': 'www.jd.com', 'expiry': 1729353305, 'httpOnly': False, 'name': 'o2State', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '{%22webp%22:true%2C%22avif%22:true}'}, {'domain': '.jd.com', 'expiry': 1723737339, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQ'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': False, 'name': 'pin', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'jd_liPodPFvasNd'}, {'domain': '.jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171'}, {'domain': '.jd.com', 'expiry': 1729353340, 'httpOnly': False, 'name': 'pinId', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'AXritTa-DsiYN22YVHMrSA'}, {'domain': '.jd.com', 'expiry': 1728921305, 'httpOnly': False, 'name': '3AB9D23F7A4B3CSS', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'jdd03K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQAAAAMLJXGCBIAAAAAAD7JR52X6R47PLAX'}, {'domain': '.jd.com', 'expiry': 1698422105, 'httpOnly': False, 'name': 'PCSYCityID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'CN_430000_431300_0'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': True, 'name': '_pst', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'jd_liPodPFvasNd'}, {'domain': '.jd.com', 'expiry': 1698681305, 'httpOnly': False, 'name': 'ipLoc-djd', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18-1586-0-0'}, {'domain': '.jd.com', 'expiry': 1699113304, 'httpOnly': False, 'name': '__jdv', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171|direct|-|none|-|1697817304358'}, {'domain': '.jd.com', 'expiry': 1732377306, 'httpOnly': False, 'name': 'shshshfpx', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ad720122-63bd-eb00-c92a-d0e9917811bd-1697817306'}, {'domain': '.jd.com', 'expiry': 1732377344, 'httpOnly': False, 'name': 'shshshfpa', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ad720122-63bd-eb00-c92a-d0e9917811bd-1697817306'}, {'domain': '.jd.com', 'expiry': 1698422140, 'httpOnly': True, 'name': 'flash', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2_XqAO-rNF16NmZlqY-GMii3zLAPtYHT-DxSrkmBtceywGaPyXu_Jz81Kswtk3DxG2CPhlO4bpfd5QSQU7Ra5EKHL9GpRMQT_O9yuW8wt-vsh*'}, {'domain': '.jd.com', 'expiry': 1698681305, 'httpOnly': False, 'name': 'areaId', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18'}, {'domain': '.jd.com', 'expiry': 1698422140, 'httpOnly': True, 'name': 'thor', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'CBCAEAA62FC15516429E3BA04D9807AFA91B9A8C52D840C07A5147175AB3448680311659AF18405C65E277182CA944E6D6E3B6336E5A73C57A90B0700BFB9924F333CD37C7A0CB6B4A9641D949D6A318A1C1AA4B2A607CBFD8A942524F3A5EB86DA8122199E6928C8293295B2E8B7F069DF6F53DEF283FD48A254C1E781139387D94DE894FA2B3E539029D6919633E40945F309E5D41787E2FF2B5E297AF7EF8'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': False, 'name': '_tp', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'NOuCMHdN5wgoS%2BBYqWNF5g%3D%3D'}, {'domain': '.jd.com', 'httpOnly': False, 'name': 'ceshi3.com', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '000'}, {'domain': '.jd.com', 'expiry': 1697817425, 'httpOnly': False, 'name': '_gia_d', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}, {'domain': '.jd.com', 'expiry': 1713369357, 'httpOnly': False, 'name': '__jdu', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '16978173043551234917588'}]'''
    option=webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    driver = webdriver.Chrome(chrome_options=option)

    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get('https://www.jd.com/')
    time.sleep(10)
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url1)
    time.sleep(10)
    url2 = str(driver.current_url)
    phonehref = url2
    driver.quit()

    r1 = requests.get(url2, headers=headers).text

    be1 = BeautifulSoup(r1, features="lxml")
    img = be1.select('div[class="spec-items"] ul[class="lh"] li[class="img-hover"]')
    image_url = re.findall(r'src="(.*?)"', str(img),re.S)
    https_image_url = ['https:' + url for url in image_url]
    https_image_url1=https_image_url[0].replace('[','').replace(']','')
    response = requests.get(https_image_url1,stream=True)
    if response.status_code == 200:
        file = phonename[0].replace('[', '').replace(']', '')
        if os.path.isfile('.data/picture'):  # 检查文件是否已存在
            print('Image already exists. No need to download again.')
        else:
            with open(f'data/picture/{file}.jpg', 'wb') as f:
                    f.write(response.content)
    else:
        print(f'Failed to download image. HTTP response code: {response.status_code}')
    ul = be1.select('ul[class="parameter2 p-parameter-list"] li ')
    brand = re.findall(r">(.*?)</a>", str(be1.select('ul[class="p-parameter-list"] li a')), re.S)
    cpu = re.findall(r">CPU型号：(.*?)</li>", str(ul), re.S)
    charging = re.findall(r">充电功率：(.*?)</li>", str(ul), re.S)
    waterproof = re.findall(r">三防标准：(.*?)</li>", str(ul), re.S)
    screen = re.findall(r">屏幕材质：(.*?)</li>", str(ul), re.S)
    characteristic = re.findall(r">特征特质：(.*?)</li>", str(ul), re.S)
    info = []
    item = {
        'brand': brand,
        'phonename': phonename,
        'cpu': cpu,
        'charging': charging,
        'waterproof': waterproof,
        'screen': screen,
        'characteristic': characteristic,
        'phonehref': phonehref,
    }
    print(item)
    info.append(item)
    '''with open('data/PhoneInfo.csv', 'a', encoding='utf-8',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['brand','phonename', 'cpu', 'charging', 'waterproof', 'screen', 'characteristic',
                                                  'phonehref'])
        if file.tell()==0:
            writer.writeheader()
        writer.writerows(info)'''
