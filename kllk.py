import json

import requests


def get_price(sid):
    url = 'https://item.jd.com/' + 100051092880	#sid就是商品url链接的那串数字，比如：https://item.jd.com/4526055.html,4526055就是sid
    headers = {
        'authority': 'p.3.cn',
        'method': 'GET',
        'path': '/' + url.split('/')[-1],
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    jsons = json.loads(response.text[0:-1])
    price = jsons[0]['p']
    if price == '-1.00':
        return "商品已售完"
    else:
        return price
