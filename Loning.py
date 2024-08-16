import time
from time import sleep
from selenium import webdriver


def get_cookies():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.implicitly_wait(5)
    url='https://www.jd.com'
    driver.get(url)
    driver.find_element_by_class_name('link-login').click()
    driver.find_element_by_id('pwd-login').click()
    username=driver.find_element_by_id('loginname')
    username.clear()
    username.send_keys('18718751065')
    password=driver.find_element_by_id('nloginpwd')
    password.clear()
#    password.send_keys('')
    sleep(50)
    cookies=driver.get_cookies()
    print(cookies)
'''def TaoBaoget_cookie():
    cookies=[{'domain': '.taobao.com', 'expiry': 1713509405, 'httpOnly': False, 'name': 'tfstk', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'dZzBphilvpvQtRiJ8w1aCbYsOQ353J_2RQG8i7Lew23peLFxQU5n8g07FAwoLDuLPlY7i74Ft45n-W0oytWVu8N3t40jit7Vn_zGM4BV3Z74tW0oyk8RMB60SP1I0xOutKgV_YiIHWs2yUa6uDMY9AT-sP6NxEkbYAxy1mYS1x5113xu3LmNS'}, {'domain': '.taobao.com', 'expiry': 1713509405, 'httpOnly': False, 'name': 'l', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'fBr-ScjcP_LjD-woBOfaFurza77OSIRYYuPzaNbMi9fPOUfB54ulW13JutL6C3GcFs1XR3cDK4dwBeYBq7NSnxvtIosM_CkmndLHR35..'}, {'domain': '.taobao.com', 'expiry': 1713509401, 'httpOnly': False, 'name': 'isg', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'BFFRggsB0FQZ-DxAZYZuGYKZYF3rvsUwEe5K7TPmTZg32nEsew7VAP84eK88VV1o'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'uc1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'cookie21=Vq8l%2BKCLiYYu&existShop=false&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&pas=0&cookie14=Uoe9agxjBoLsUA%3D%3D&cookie15=UtASsssmOIJ0bQ%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_nk_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb942068347144'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_l_g_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'Ug%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'B0Flg37oF3%2B0U3BTZvQCNc4MD9ue4vzczJYOFULy0Lg%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'dnk', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb942068347144'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'cancelledSubSites', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'empty'}, {'domain': '.taobao.com', 'expiry': 1698591002, 'httpOnly': False, 'name': 'mt', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ci=0_1'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'sg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '46f'}, {'domain': '.taobao.com', 'expiry': 1700578201, 'httpOnly': False, 'name': 'lgc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb942068347144'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'csg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '27f5f469'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'skt', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2a810c5f262688bb'}, {'domain': '.taobao.com', 'expiry': 1700578201, 'httpOnly': True, 'name': 'uc4', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'id4=0%40U2gqy1hn5r4dtVRw9bqlN0lnjxE8NydO&nk4=0%40FY4HWGytN4J5LUDJ9zTKpFSGFhD14jZSPw%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '19d48be13222649e576a646277559f2e'}, {'domain': '.taobao.com', 'expiry': 1729522201, 'httpOnly': True, 'name': 'sgcookie', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'E100LvHrWehp0aqh1KVqcbDgCVAf3Dr8XLX6%2F%2BtxcqHpzfVX5EkV0VdaKPwPviSwjcMi5cwRH%2B2akHzG6yuCrYYpRXceL3lBhHnOiwgYfYCemUU%3D'}, {'domain': '.taobao.com', 'expiry': 1729522201, 'httpOnly': False, 'name': '_cc_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'Vq8l%2BKCLiw%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie17', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'UUpgRKmfspk7hHrn6g%3D%3D'}, {'domain': '.taobao.com', 'expiry': 1698216594, 'httpOnly': False, 'name': 'xlly_s', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1'}, {'domain': '.taobao.com', 'expiry': 1729522201, 'httpOnly': False, 'name': 'tracknick', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb942068347144'}, {'domain': '.taobao.com', 'expiry': 1729493402, 'httpOnly': False, 'name': 'thw', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'cn'}, {'domain': '.taobao.com', 'expiry': 1732517393, 'httpOnly': False, 'name': 'cna', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ELS7HW6Ar2QCAXjknlNYjNOc'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'unb', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2212433670836'}, {'domain': '.taobao.com', 'expiry': 1700578201, 'httpOnly': True, 'name': 'uc3', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'id2=UUpgRKmfspk7hHrn6g%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&nk2=F5RMHUbb3LtS%2B25HchM%3D&vt3=F8dD3CAYz3LUsUluKcc%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_tb_token_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '7b3e5f643458e'}, {'domain': '.taobao.com', 'expiry': 1705762201, 'httpOnly': False, 'name': 't', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ed6a0bec2529da515ec52cc1db43da79'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'existShop', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'MTY5Nzk1NzQwMA%3D%3D'}, {'domain': '.taobao.com', 'expiry': 1698562193, 'httpOnly': False, 'name': '_m_h5_tk', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'bbb55a8fb15d5a3d60b410fc43314712_1697965672623'}, {'domain': '.taobao.com', 'expiry': 1698562193, 'httpOnly': False, 'name': '_m_h5_tk_enc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '5caa3a73d66a5ad14d5f7c976a533b15'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': '_samesite_flag_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'true'}]
    goods = input("请输入想要搜索的商品：")
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.implicitly_wait(10)
    url = 'https://www.taobao.com/'
    driver.get(url)
    time.sleep(10)
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    start_url = 'https://s.taobao.com/search?q=' + goods
    driver.get(start_url)
    time.sleep(10)
    driver.quit()'''






if __name__ == '__main__':
    get_cookies()
    sleep(10)