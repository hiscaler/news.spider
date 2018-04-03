# -*- encode: utf-8 -*-
"""CNN 网站数据地址采集
"""
import time

from browser import Browser
from helper import post_urls

base_url = 'https://edition.cnn.com'
language = 'en-US'

source_urls = [
    'https://edition.cnn.com/',
    'https://edition.cnn.com/travel',
]

begin_time = time.time()
try:
    browser = Browser()
    browser.open()
    open_browser_time = time.time()
    for url in source_urls:
        browser.get(url)
        html = browser.page_source(url)
        if html:
            page_urls = browser.get_all_links(html, lambda href: href and href.endswith('index.html'))
            post_urls(page_urls, language)
        else:
            print("获取 {url} 源码失败。".format(url=url))

finally:
    browser.close()

print("Open browser cost %s seconds" % (open_browser_time - begin_time))
print("Total cost %s Seconds" % (time.time() - begin_time))
