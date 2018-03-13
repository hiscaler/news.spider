# -*- coding: utf-8 -*-
import io
import re
import sys

import scrapy
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


class BaiduBaike(scrapy.Spider):
    name = 'baidu_baike'
    page_index = 1

    start_urls = [
        'https://baike.baidu.com/item/中国'
    ]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Host': 'bj.zu.anjuke.com',
    }

    countries = {
        '中国': 2,
        '美国': 3,
        '日本': 4,
        '英国': 5,
    }

    category_id = None

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        name = None
        obj = soup.select_one('dd.lemmaWgt-lemmaTitle-title')
        if obj is not None:
            name = re.findall(r"<h1.*>(.*)</h1>", str(obj))
            if name is not None:
                name = name[0]

        description = soup.select_one('div.lemma-summary')
        if description is not None:
            description = description.extract().get_text()
        else:
            description = None

        if name is not None:
            if self.category_id is None:
                self.category_id = self.countries[name]
                self.countries.pop(name)
        else:
            self.category_id = None

        yield {
            'id': self.category_id,
            'name': name,
            'description': description
        }

        if len(self.countries):
            country = self.countries.popitem()
            self.category_id = country[1]
            next_page_url = "https://baike.baidu.com/item/" + country[0]
            yield scrapy.Request(response.urljoin(next_page_url))
