# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re


class SogouFanyi(scrapy.Spider):
    name = 'sogou_fanyi'
    page_index = 1

    start_urls = [
        'https://translate.sogoucdn.com/pcvtsnapshot?url=https%3A%2F%2Fwww.msn.com%2Fen-us%2Fnews%2Fpolitics%2Ftrump-takes-victory-lap-on-mccabe-firing-a-great-day-for-democracy%2Far-BBKkbJX%3Fli%3DBBnbcA1&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240'
    ]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=D:/tmp')
        browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)

        browser.get(self.start_urls[0])

        browser.switch_to.frame('translate-iframe-dest')
        time.sleep(10)
        browser.execute_script('window.localStorage.setItem("TRANSPAGE_DIALOG_SHOW", 1);')

        page_source = browser.page_source
        parse_result = self.parse_msn(page_source)
        print(parse_result)
        # print(page_source)
        # soup = BeautifulSoup(page_source)
        # obj = soup.select_one('div.articlecontent > h1')
        # print(obj)
        browser.close()

    def parse_msn(self, page_source):
        if page_source:
            soup = BeautifulSoup(page_source)
            title = soup.select_one('div.articlecontent > h1').get_text()
            content = soup.select_one('div.richtext')
            description = content.get_text().replace("\n", '')[:60]
            return {
                'title': title,
                'description': description,
                'content': content
            }
        else:
            return None

    def parse(self, response):
        if not response or response is None:
            return

        print(response)

        raw_data = response.xpath('//div[@class="articlecontent"]')
        print(raw_data)
