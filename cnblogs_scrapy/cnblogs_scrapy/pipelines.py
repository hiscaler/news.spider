# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CnblogsScrapyPipeline(object):
    def open_spider(self, spider):
        self.fp = open("data.list", 'w')

    def close_spider(self, spider):
        self.fp.close()

    def process_item(self, item, spider):
        self.fp.write(item["article_title"] + "\n")
        self.fp.write(item["article_view"] + "\n")
        self.fp.write(item["post_date"] + "\n")
        self.fp.write(item["article_summary"] + "\n")
        return item
