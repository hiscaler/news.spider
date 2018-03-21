# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pprint
import requests
import datetime


class SogouPipeline(object):
    remote_api_url = None

    def __init__(self):
        self.remote_api_url = 'http://192.168.1.222:8066/index.php/news?accessToken=FF78F2D3-C2A5-2875-0EE2-EB6803A67639'

    def process_item(self, item, spider):
        if item['title'] is not None or item['content'] is not None:
            if 'node_id' not in item or not item['node_id']:
                item['node_id'] = 0

            if 'description' not in item or not item['description']:
                item['description'] = item['content'].strip().replace("\n", '')[:60]

            if 'short_title' not in item or not item['short_title']:
                item['short_title'] = item['title']

            if 'published_at' not in item or not item['published_at']:
                item['published_at'] = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')

            if 'author' not in item or not item['author']:
                item['author'] = 'APD'

            if 'source' not in item or not item['source']:
                item['source'] = 'APD'

            print(80 * '#')
            print(self.__class__.__name__ + '.' + self.process_item.__name__ + ':')
            print(80 * '-')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(item)

            id = item['id']
            del item['id']

            # 修改采集地址状态为完成
            response = requests.post('http://localhost:8002/index.php/api/post/url/status?id=' + str(id), data={'status': 'finished'})
            if response.reason == 'Ok':
                body = response.json()
                if not body.success:
                    print(response.error.message)

            else:
                print(response)

            response = requests.post(url=self.remote_api_url, data=item)
            print(response.content)
            if response.reason == 'Ok':
                print(response.content)
            else:
                print("Post to `%s` failed." % self.remote_api_url)

            print(80 * '#')
            return item
        else:
            print("Item is invalid.")
