# -*- coding: utf-8 -*-

import requests
import scrapy
from bs4 import BeautifulSoup
from thepaper.items import ThepaperItem
import re


class Thepaper(scrapy.Spider):
    name = 'thepaper'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    page = 1

    last_time = 'nothing'

    start_urls = [
        "http://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2014625,2013382,2014629,2014464,&pageidx=" + str(page) + "&lasttime=nothing"
    ]

    # def start_requests(self):
    #     url = "http://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2014625,2013382,2014629,2014464,&pageidx=" + str(self.page) + "&lasttime=" + self.last_time
    #     yield Request(url, headers=self.headers)

    def parse(self, response):
        if not response or response is None:
            return

        raw_data = response.xpath('//div[@class="news_li"]')

        for data in raw_data:
            item = ThepaperItem()

            title = data.xpath("h2/a/text()").extract_first().strip()
            summary = data.xpath("p/text()").extract()
            category = data.xpath("div[@class='pdtt_trbs']/a/text()").extract_first().strip()
            if len(category):
                summary = summary[0].strip()
            else:
                summary = ""
            href = data.xpath("h2/a/@href").extract_first().strip()
            url = ''
            content = ''
            if (href):
                url = 'http://www.thepaper.cn/' + href
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text)
                    obj = soup.select_one('div.news_txt')
                    if obj is not None:
                        content_list = re.findall(r"<div class=\"news_txt\".*?>(.*)</div>", str(obj))
                        if content_list:
                            content = content_list[0]

                else:
                    content = ''

            if not content:
                continue

            item['url'] = url
            item['title'] = title
            item['summary'] = summary
            item['category'] = category
            item['content'] = content

            # print(item)

            yield item

        self.page += 1
        if self.page <= 100:
            next_page_url = "http://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2014625,2013382,2014629,2014464,&pageidx=" + str(self.page) + "&lasttime=" + self.last_time
        else:
            next_page_url = None

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
