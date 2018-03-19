# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from urllib import parse


class SogouFanyi(scrapy.Spider):
    name = 'sogou_fanyi'
    debug = True
    page_index = 1
    # 'https://translate.sogoucdn.com/pcvtsnapshot?url=https%3A%2F%2Fwww.msn.com%2Fen-us%2Fnews%2Fpolitics%2Ftrump-takes-victory-lap-on-mccabe-firing-a-great-day-for-democracy%2Far-BBKkbJX%3Fli%3DBBnbcA1&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240',
    start_urls = [
        # 'http://www.bbc.com/news/world-us-canada-43453312'
        'https://finance.yahoo.com/news/thanks-obama-virginia-blames-barack-060948297.html'
    ]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=D:/tmp')
        browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)

        url = self.start_urls[0]
        print(url)
        sogou_url = ('https://translate.sogoucdn.com/pcvtsnapshot?url=%s&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240' % parse.quote(url, ''))
        print(sogou_url)

        browser.get(sogou_url)

        browser.switch_to.frame('translate-iframe-dest')
        time.sleep(20)
        browser.execute_script('window.localStorage.setItem("TRANSPAGE_DIALOG_SHOW", 1);')
        time.sleep(20)

        page_source = browser.page_source
        if self.debug:
            f = open('article.txt', 'w+')
            f.write(page_source)
            f.close()

        if url is None:
            parse_result = None
        elif '.bbc.' in url:
            parse_result = self.parse_bbc(page_source)
        elif '.msn.' in url:
            parse_result = self.parse_msn(page_source)
        elif '.yahoo.' in url:
            parse_result = self.parse_yahoo(page_source)
        else:
            parse_result = None

        if parse_result is not None:
            print("Translate success, Return value is:")
            print(parse_result)
            # Post to api
        else:
            print('Translate Failed.')
        browser.close()

    def parse_msn(self, page_source):
        """
        Parse www.msn.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
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

    def parse_bbc(self, page_source):
        """
        Parse www.bbc.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
        if page_source:
            soup = BeautifulSoup(page_source)
            title = soup.select_one('h1.story-body__h1').get_text()
            content = soup.select_one('div.story-body')
            description = content.get_text().replace("\n", '')[:60]
            return {
                'title': title,
                'description': description,
                'content': content
            }
        else:
            return None

    def parse_yahoo(self, page_source):
        """
        Parse www.yahoo.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
        if page_source:
            soup = BeautifulSoup(page_source)
            title = soup.select_one('#SideTop-0-HeadComponentTitle h1')
            if title is not None:
                title = title.get_text()

            content = soup.select_one('div.canvas-body')
            if content is not None:
                print(content)
                description = content.get_text().replace("\n", '')[:60]

            if title is None or content is None:
                return None
            else:
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
