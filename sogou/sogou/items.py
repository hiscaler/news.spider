# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SogouItem(scrapy.Item):
    post_url_id = scrapy.Field()
    node_id = scrapy.Field()
    title = scrapy.Field()
    short_title = scrapy.Field()
    keywords = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    description = scrapy.Field()
    published_at = scrapy.Field()
    content = scrapy.Field()
    raw_content = scrapy.Field()
