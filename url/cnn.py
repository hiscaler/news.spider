# -*- encode: utf-8 -*-
"""CNN 网站数据地址采集
"""
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://edition.cnn.com/'
language = 'en-US'

urls = [
    'https://edition.cnn.com/',
    'https://edition.cnn.com/travel',
]

begin_time = time.time()
try:
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=D:/tmp')
    options.add_argument('-headless')
    options.add_argument('-disable-gpu')
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)
    open_browser_time = time.time()
    for url in urls:
        browser.get(url)
        html = browser.page_source
        if html:
            soup = BeautifulSoup(html)
            for script in soup(["script", "style"]):
                script.decompose()

            links = soup.find_all('a', href=True)
            pattern = re.compile(r'.*href="(\S*)".*')
            for link in links:
                link = link.prettify()
                href = pattern.findall(link)
                if href:
                    href = href[0]
                    if href and href.endswith('index.html'):
                        if not href.startswith('http'):
                            href = url + href

                        print("Url: %s" % href)

                        response = requests.post('http://localhost:8002/index.php/api/post/url/create', data={"language": language, "url": href})
                        if response.ok:
                            body = response.json()
                            if body['success']:
                                print("Success: %s" % href)
                            else:
                                print("Failed: %s" % href)
                        else:
                            print(response.text)
finally:
    browser.close()

print("Open browser cost %s seconds" % (open_browser_time - begin_time))
print("Cost %s Seconds" % (time.time() - begin_time))
