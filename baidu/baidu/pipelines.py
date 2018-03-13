# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests


class BaiduPipeline(object):
    def process_item(self, item, spider):
        if item['id'] and item['name'] is not None and item['description'] is not None:
            r = requests.post('http://localhost:8002/index.php/api/category/update?id=' + str(item['id']), {
                'description': item['description']
            })
            if r.status_code == 200:
                print(r.content)
            else:
                print(r.content)

        return item
