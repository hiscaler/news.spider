# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from thepaper.items import ThepaperItem


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
            item['title'] = title
            item['summary'] = summary
            item['category'] = category
            item['content'] = ''

            print(item)

            yield item

        self.page += 1
        if self.page <= 20:
            next_page_url = "http://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2014625,2013382,2014629,2014464,&pageidx=" + str(self.page) + "&lasttime=" + self.last_time
        else:
            next_page_url = None

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
