# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SogouItem(scrapy.Item):
    id = scrapy.Field()
    node_id = scrapy.Field()
    title = scrapy.Field()
    short_title = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    published_at = scrapy.Field()
    content = scrapy.Field()
