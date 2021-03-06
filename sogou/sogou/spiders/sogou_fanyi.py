# -*- coding: utf-8 -*-

import io
import sys
import time
from urllib import parse

import os
import requests
import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from sogou.items import SogouItem
from scrapy.utils.project import get_project_settings

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


class SogouFanyi(scrapy.Spider):
    name = 'sogou_fanyi'
    debug = True
    browser = None
    urls = []
    url_index = None

    # 'https://translate.sogoucdn.com/pcvtsnapshot?url=https%3A%2F%2Fwww.msn.com%2Fen-us%2Fnews%2Fpolitics%2Ftrump-takes-victory-lap-on-mccabe-firing-a-great-day-for-democracy%2Far-BBKkbJX%3Fli%3DBBnbcA1&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240',
    # start_urls = [
    #     # 'http://www.bbc.com/news/world-us-canada-43453312'
    #     'https://finance.yahoo.com/news/thanks-obama-virginia-blames-barack-060948297.html'
    # ]

    def start_requests(self):
        # urls = [
        #     'http://www.bbc.com/news/world-us-canada-43453312'
        #     'https://finance.yahoo.com/news/thanks-obama-virginia-blames-barack-060948297.html'
        # ]
        url_item = self.urls[self.url_index]
        print("Current url index is %s" % self.url_index)
        print("Current url is %s" % url_item['url'])
        yield scrapy.Request(url=url_item['url'], callback=self.parse)
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse())

    def __init__(self):
        super(SogouFanyi, self).__init__()
        if not self.urls:
            settings = get_project_settings()
            api = settings['BIZ_API']['dev'] if settings['BIZ_DEBUG'] else settings['BIZ_API']['prod']
            response = requests.get(api['postUrl'] + '/post/url/list?limit=100&status=pending')
            if response.status_code == 200:
                body_json = response.json()
                for item in body_json['data']['items']:
                    self.urls.append({'id': item['id'], 'url': item['url']})
                print("body_json type is: %s" % type(body_json))
                print(body_json)
            else:
                self.urls.append({'id': 0, 'url': 'http://www.example.com'})
                # self.urls = [
                #     # 'http://www.bbc.com/news/world-us-canada-43453312',
                #     'https://finance.yahoo.com/news/thanks-obama-virginia-blames-barack-060948297.html',
                #     'https://finance.yahoo.com/news/u-supreme-court-rejects-arizona-challenge-dreamers-program-134912301.html',
                # ]

        self.url_index = 0
        # todo Get urls from api
        # sogou_url = ('https://translate.sogoucdn.com/pcvtsnapshot?url=%s&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240' % parse.quote(self.start_urls[0], ''))
        # self.start_urls.clear()
        # self.start_urls.append(sogou_url)
        # options = webdriver.ChromeOptions()
        # options.add_argument('user-data-dir=D:/tmp')
        # self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)
        # self.start_urls = []
        """
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=D:/tmp')
        browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)

        url = self.start_urls[0]

        print(url)
        sogou_url = ('https://translate.sogoucdn.com/pcvtsnapshot?url=%s&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240' % parse.quote(url, ''))
        self.start_urls.append(sogou_url)
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
        """

    def parse_msn(self, page_source):
        """
        Parse www.msn.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
        if page_source:
            soup = BeautifulSoup(page_source, 'lxml')
            for script in soup(["script", "style"]):
                script.decompose()

            title = soup.select_one('div.articlecontent > h1')
            if title:
                title = title.get_text().strip()
            content = soup.select_one('div.richtext')
            if content:
                description = content.get_text().strip().replace("\n", '')[:60]
                content = content.prettify()
            else:
                description = None
            item = SogouItem()
            item['title'] = title
            item['source'] = 'msn'
            item['description'] = description
            item['content'] = content

            return item
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
            for script in soup(["script", "style"]):
                script.decompose()

            title = soup.select_one('h1.story-body__h1')
            if title:
                title = title.get_text().strip()
            content = soup.select_one('div.story-body')
            if content:
                description = content.get_text().strip().replace("\n", '')[:60]
                content = content.prettify()
            else:
                description = None
            item = SogouItem()
            item['title'] = title
            item['source'] = 'bbc'
            item['description'] = description
            item['content'] = content

            return item
        else:
            return None

    def parse_yahoo(self, page_source):
        """
        Parse www.yahoo.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
        if page_source:
            title = None
            soup = BeautifulSoup(page_source)
            for script in soup(["script", "style"]):
                script.decompose()

            selectors = ['#Lead-1-HeadComponentTitle h1', '#SideTop-0-HeadComponentTitle h1']
            for selector in selectors:
                title = soup.select_one(selector)
                if title is None:
                    continue
                else:
                    title = title.get_text().strip()
                    break

            content = soup.select_one('div.canvas-body')
            raw_content = content
            if content:
                description = content.get_text().strip().replace("\n", '')[:60]
                print("Yahoo content type = %s" % content)
                content = content.prettify()
            else:
                description = None

            if title is None or content is None:
                return None
            else:
                item = SogouItem()
                item['title'] = title
                item['source'] = 'yahoo'
                item['description'] = description
                item['raw_content'] = raw_content
                item['content'] = content

                return item
        else:
            return None

    def parse_cnn(self, page_source):
        """
        Parse www.cnn.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
        if page_source:
            soup = BeautifulSoup(page_source)
            for script in soup(["script", "style"]):
                script.decompose()

            title = None
            selectors = ['h1.article-title', 'h1.pg-headline']
            for selector in selectors:
                title = soup.select_one(selector)
                if title is None:
                    continue
                else:
                    title = title.get_text().strip()
                    break

            content = soup.select_one('div#storytext')
            if content:
                description = content.get_text().strip().replace("\n", '')[:60]
                content = content.prettify()
            else:
                description = None

            if title is None or content is None:
                return None
            else:
                item = SogouItem()
                item['title'] = title
                item['source'] = 'yahoo'
                item['description'] = description
                item['content'] = content

                return item
        else:
            return None

    def parse_reuters(self, page_source):
        """
        Parse www.reuters.com article content

        :param page_source: article content
        :return: return dict if parse success, else return None
        """
        if page_source:
            soup = BeautifulSoup(page_source)
            for script in soup(["script", "style"]):
                script.decompose()

            title = soup.select_one('div.foreground > h1')
            if title:
                title = title.get_text().strip()

            content = soup.select_one('div.body_1gnLA')
            if content:
                description = content.get_text().strip().replace("\n", '')[:60]
                content = content.prettify()
            else:
                description = None

            if title is None or content is None:
                return None
            else:
                item = SogouItem()
                item['title'] = title
                item['source'] = 'yahoo'
                item['description'] = description
                item['content'] = content

                return item
        else:
            return None

    def parse(self, response):
        try:
            url = response.url
            options = webdriver.ChromeOptions()
            options.add_argument('user-data-dir=D:/tmp')
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver', options=options)
            print("Response.url = %s" % url)
            # sogou_url = ('https://translate.sogoucdn.com/pcvtsnapshot?url=%s&query=&tabMode=1&noTrans=0&tfr=web_en&from=en&to=zh-CHS&_t=1521270440240' % parse.quote(url, ''))
            sogou_url = ('http://translate.sogoucdn.com/pcvtsnapshot?from=auto&to=zh-CHS&tfr=translatepc&url=%s&domainType=sogou' % parse.quote(url, ''))

            print("Sogou URL = %s" % sogou_url)
            self.browser.get(sogou_url)

            self.browser.switch_to.frame('translate-iframe-dest')
            time.sleep(20)
            self.browser.execute_script('window.localStorage.setItem("TRANSPAGE_DIALOG_SHOW", 1);')
            time.sleep(20)

            page_source = self.browser.page_source
            print("page_source type is " + str(type(page_source)))
            if self.debug and page_source:
                f = open('article.txt', 'w+')
                # print(page_source)
                # f.write(page_source.encode('utf-8'))
                f.close()

            if url is None:
                parse_result = None
            elif '.bbc.' in url:
                parse_result = self.parse_bbc(page_source)
            elif '.msn.' in url:
                parse_result = self.parse_msn(page_source)
            elif '.yahoo.' in url:
                parse_result = self.parse_yahoo(page_source)
            elif '.cnn.' in url:
                parse_result = self.parse_cnn(page_source)
            elif '.reuters.' in url:
                parse_result = self.parse_reuters(page_source)
            else:
                parse_result = None

            if parse_result is not None:
                parse_result['post_url_id'] = self.urls[self.url_index]['id']
                parse_result['source_url'] = url
                yield parse_result
                # Post to api
            else:
                yield {
                    'error': True,
                    'post_url_id': self.urls[self.url_index]['id']
                }

            self.url_index = self.url_index + 1
            print('self.url_index = ' + str(self.url_index))
            if len(self.urls) > self.url_index:
                url = self.urls[self.url_index]
                print('Continue url is %s' % url)
                yield scrapy.Request(url=url['url'], callback=self.parse)
                # yield response.follow(url, self.parse())
        finally:
            if self.browser is not None:
                self.browser.close()
            time.sleep(10)
