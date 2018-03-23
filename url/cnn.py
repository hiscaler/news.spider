# -*- encode: utf-8 -*-


import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://edition.cnn.com/'
language = 'en-US'
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=D:/tmp')
# options.add_argument('-headless')
browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)
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

browser.close()
