# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pprint


class SogouPipeline(object):
    def process_item(self, item, spider):
        if item['title'] is not None or item['content'] is not None:
            if not item['description']:
                item['description'] = item['content'].strip().replace("\n", '')[:60]

            print(80 * '#')
            print(self.__class__.__name__ + '.' + self.process_item.__name__ + ':')
            print(80 * '-')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(item)
            print(80 * '#')
            return item
        else:
            print("Item is invalid.")
