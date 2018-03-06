import scrapy

from jfdaily.items import JfdailyItem


class Jfdaily(scrapy.Spider):
    name = 'jfdaily'

    page = 1

    start_urls = [
        "http://www.jfdaily.com/news/sublist?section=1&page=" + str(page)
    ]

    def parse(self, response):
        if not response or response is None:
            return

        raw_data = response.xpath('//div[@class="chengshi"]')

        for data in raw_data:
            item = JfdailyItem()
            title = data.xpath('div[@class="chengshi_wz_h"]/a/text()')
            item['title'] = title
            print(title)

            yield item

        self.page += 1
        if self.page <= 1:
            next_page_url = "http://www.jfdaily.com/news/sublist?section=1&page=" + str(self.page)
        else:
            next_page_url = None

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
