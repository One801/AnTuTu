import csv
import os.path
import requests
import re
import time
import random

from bs4 import BeautifulSoup
from selenium import webdriver

#url = ' https://www.antutu.com/ranking/rank1.htm'#Android性能
#url = ' https://www.antutu.com/ranking/rank2.htm'#Android性价比
#url='https://www.antutu.com/ranking/judge.htm'#Android好评
#url='https://www.antutu.com/ranking/ios.htm'#ios性能
url = 'https://www.antutu.com/ranking/judgeios.htm'  # ios好评

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
r = requests.get(url, headers=headers)
r.encoding = "utf-8"
be = BeautifulSoup(r.text, features="lxml")

print(url)
'''C = be.select('ul[class="list-unstyled newrank-b"] a')
name = be.select('ul[class="list-unstyled newrank-b"] a div li[class="bfirst"]')#性能'''
C = be.select('ul[class="list-unstyled newrankxjb newrankxjb-b"] a')
name = be.select('ul[class="list-unstyled newrankxjb newrankxjb-b"] a div li[class="newrankc"]')  # 性价比，好评
a = 0
for i in range(0, 41):  # 117，72，62￥43，41
    #phonename = re.findall(r'</span>(.*?)<span', str(name[a]), re.S)
    phonename = re.findall(r'</span>(.*?)</li', str(name[a]), re.S)  # 好评
    # 手机名称
    rankhref = C[a].get('href')
    a += 1
    # print(mobilehref)
    url1 = rankhref
    # webbrowser.get('chrome').open(url1,new=1,autoraise=True)
    cookies =[{'domain': 'www.jd.com', 'expiry': 1698372811, 'httpOnly': False, 'name': 'UseCorpPin', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'}, {'domain': '.jd.com', 'expiry': 1732929211, 'httpOnly': False, 'name': 'shshshfpb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'AAjmPsW6LEmLTBcxlmCl1NWXBYiBMdBaYNpGXQAAAAAA'}, {'domain': '.jd.com', 'expiry': 1698371010, 'httpOnly': False, 'name': '__jdb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171.3.1698369196496833862171|1.1698369196'}, {'domain': '.jd.com', 'expiry': 1713921210, 'httpOnly': False, 'name': '__jda', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171.1698369196496833862171.1698369196.1698369196.1698369196.1'}, {'domain': '.jd.com', 'expiry': 1700961210, 'httpOnly': False, 'name': 'unick', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'}, {'domain': '.jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171'}, {'domain': '.jd.com', 'expiry': 1729905210, 'httpOnly': False, 'name': 'pinId', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '9AtnzikIiXEpN177ctDmyg'}, {'domain': '.jd.com', 'expiry': 1700961210, 'httpOnly': False, 'name': 'pin', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'}, {'domain': '.jd.com', 'expiry': 1713921231, 'httpOnly': False, 'name': '__jdu', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1698369196496833862171'}, {'domain': '.jd.com', 'expiry': 1732929210, 'httpOnly': False, 'name': 'TrackID', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '18SAVRnUG7m4BsJ6FiT9rS7iagrIIobPXDUotN2dUgj0_gF4ZQb38rmhoeusqrtS6DtEOvUE0EEdcX711rgFsgs49SBWpNl5HJQwIBrXRZ7w'}, {'domain': '.jd.com', 'expiry': 1724289198, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQ'}, {'domain': 'www.jd.com', 'expiry': 1729905197, 'httpOnly': False, 'name': 'o2State', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '{%22webp%22:true%2C%22avif%22:true%2C%22lastvisit%22:1698369197335}'}, {'domain': '.jd.com', 'expiry': 1700961210, 'httpOnly': True, 'name': '_pst', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '%E4%BD%9F%E5%BF%83%E5%AE%97'}, {'domain': '.jd.com', 'expiry': 1699233197, 'httpOnly': False, 'name': 'ipLoc-djd', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18-1586-0-0'}, {'domain': '.jd.com', 'expiry': 1699665196, 'httpOnly': False, 'name': '__jdv', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171|direct|-|none|-|1698369196496'}, {'domain': '.jd.com', 'expiry': 1732929197, 'httpOnly': False, 'name': 'shshshfpx', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '5a62d305-cc65-9829-7535-65c162204c74-1698369197'}, {'domain': '.jd.com', 'expiry': 1732929211, 'httpOnly': False, 'name': 'shshshfpa', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '5a62d305-cc65-9829-7535-65c162204c74-1698369197'}, {'domain': '.jd.com', 'expiry': 1698974010, 'httpOnly': True, 'name': 'flash', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2_lV-yRhviiP1_nkxfNhoW4IHstt_4w8Av_NAkRByKVLYPG1wLa1f9uva0EH2Me7QF3qsbv1zWn_8kQoOqTUrRJDghsz_ik4wpRKLWaXHvX5e*'}, {'domain': '.jd.com', 'expiry': 1699233197, 'httpOnly': False, 'name': 'areaId', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18'}, {'domain': '.jd.com', 'expiry': 1698974010, 'httpOnly': True, 'name': 'thor', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '7B4AFE61F6A4E8F7376A98CEF1F990904A855EEE2154A10FEDAFBFE0E1F8135F0F8D0F2D6D2D5DE0CD886F6B00873A8DBD20C63BB0C0C0A5ED5BEA25ACB9CB0FCDBB4A03EB479C544679C3E79C873EB5F5D3124AAF2FD2F216B067423D5B0E685F7BF10C178259073B2BA74FC6CB15A2B8620A525A037B4D839C017D06F8A95B'}, {'domain': '.jd.com', 'expiry': 1700961210, 'httpOnly': False, 'name': '_tp', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ilfzk4qmKQELFG9iaEwJF0ePLXlTTRyu9Ntm%2FIwkHDo%3D'}, {'domain': '.jd.com', 'httpOnly': False, 'name': 'ceshi3.com', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '000'}, {'domain': '.jd.com', 'expiry': 1729473197, 'httpOnly': False, 'name': '3AB9D23F7A4B3CSS', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'jdd03K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQAAAAMLN2YVN2IAAAAACYFKJJYBQTW6NAX'}, {'domain': '.jd.com', 'expiry': 1698369317, 'httpOnly': False, 'name': '_gia_d', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}]
    '''cookies2=[{'domain': 'www.jd.com', 'expiry': 1697820944, 'httpOnly': False, 'name': 'UseCorpPin', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'jd_liPodPFvasNd'}, {'domain': '.jd.com', 'expiry': 1732377344, 'httpOnly': False, 'name': 'shshshfpb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'AAki4zE2LEnIBImO96wDJKtDpkXgRvRaXgXMGQAAAAAA'}, {'domain': '.jd.com', 'expiry': 1697819142, 'httpOnly': False, 'name': '__jdb', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171.3.16978173043551234917588|1.1697817304'}, {'domain': '.jd.com', 'expiry': 1713369342, 'httpOnly': False, 'name': '__jda', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171.16978173043551234917588.1697817304.1697817304.1697817304.1'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': False, 'name': 'unick', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'jd_liPodPFvasNd'}, {'domain': 'www.jd.com', 'expiry': 1729353305, 'httpOnly': False, 'name': 'o2State', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '{%22webp%22:true%2C%22avif%22:true}'}, {'domain': '.jd.com', 'expiry': 1723737339, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQ'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': False, 'name': 'pin', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'jd_liPodPFvasNd'}, {'domain': '.jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171'}, {'domain': '.jd.com', 'expiry': 1729353340, 'httpOnly': False, 'name': 'pinId', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'AXritTa-DsiYN22YVHMrSA'}, {'domain': '.jd.com', 'expiry': 1728921305, 'httpOnly': False, 'name': '3AB9D23F7A4B3CSS', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'jdd03K6J4MN3Q77A4KBIDPQQZEWYPUM4ZQJ3FNOWTMDHEERA3RAQWSSESMRNSEYD7DL2M356SDJYTTTCJA5F5LIM4BKOTJQAAAAMLJXGCBIAAAAAAD7JR52X6R47PLAX'}, {'domain': '.jd.com', 'expiry': 1698422105, 'httpOnly': False, 'name': 'PCSYCityID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'CN_430000_431300_0'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': True, 'name': '_pst', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'jd_liPodPFvasNd'}, {'domain': '.jd.com', 'expiry': 1698681305, 'httpOnly': False, 'name': 'ipLoc-djd', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18-1586-0-0'}, {'domain': '.jd.com', 'expiry': 1699113304, 'httpOnly': False, 'name': '__jdv', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '76161171|direct|-|none|-|1697817304358'}, {'domain': '.jd.com', 'expiry': 1732377306, 'httpOnly': False, 'name': 'shshshfpx', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ad720122-63bd-eb00-c92a-d0e9917811bd-1697817306'}, {'domain': '.jd.com', 'expiry': 1732377344, 'httpOnly': False, 'name': 'shshshfpa', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'ad720122-63bd-eb00-c92a-d0e9917811bd-1697817306'}, {'domain': '.jd.com', 'expiry': 1698422140, 'httpOnly': True, 'name': 'flash', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2_XqAO-rNF16NmZlqY-GMii3zLAPtYHT-DxSrkmBtceywGaPyXu_Jz81Kswtk3DxG2CPhlO4bpfd5QSQU7Ra5EKHL9GpRMQT_O9yuW8wt-vsh*'}, {'domain': '.jd.com', 'expiry': 1698681305, 'httpOnly': False, 'name': 'areaId', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '18'}, {'domain': '.jd.com', 'expiry': 1698422140, 'httpOnly': True, 'name': 'thor', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'CBCAEAA62FC15516429E3BA04D9807AFA91B9A8C52D840C07A5147175AB3448680311659AF18405C65E277182CA944E6D6E3B6336E5A73C57A90B0700BFB9924F333CD37C7A0CB6B4A9641D949D6A318A1C1AA4B2A607CBFD8A942524F3A5EB86DA8122199E6928C8293295B2E8B7F069DF6F53DEF283FD48A254C1E781139387D94DE894FA2B3E539029D6919633E40945F309E5D41787E2FF2B5E297AF7EF8'}, {'domain': '.jd.com', 'expiry': 1700409340, 'httpOnly': False, 'name': '_tp', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'NOuCMHdN5wgoS%2BBYqWNF5g%3D%3D'}, {'domain': '.jd.com', 'httpOnly': False, 'name': 'ceshi3.com', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '000'}, {'domain': '.jd.com', 'expiry': 1697817425, 'httpOnly': False, 'name': '_gia_d', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}, {'domain': '.jd.com', 'expiry': 1713369357, 'httpOnly': False, 'name': '__jdu', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '16978173043551234917588'}]'''
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
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
    img = be1.select('div[class="jqzoom main-img"] img')
    image_url = re.findall(r'data-origin="(.*?)"', str(img), re.S)
    https_image_url = ['https:' + url for url in image_url]
    https_image_url1 = https_image_url[0].replace('[', '').replace(']', '')
    response = requests.get(https_image_url1, stream=True)
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
    if characteristic==[]:
        characteristic='未知'
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
        'img_url': https_image_url1,
    }
    print(item)
    info.append(item)
    with open('data/PhoneInfo.csv', 'a+', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['brand', 'phonename', 'cpu', 'charging', 'waterproof', 'screen',
                                                  'characteristic',
                                                  'phonehref', 'img_url'])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(info)