# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pprint
import requests
import datetime
import re
import mimetypes
import uuid
import os


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

            item['content'] = self.fix_content(item['content'])

            print(80 * '#')
            print(self.__class__.__name__ + '.' + self.process_item.__name__ + ':')
            print(80 * '-')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(item)

            id = item['id']
            del item['id']

            print('Post to %s' % self.remote_api_url)
            response = requests.post(url=self.remote_api_url, data=item)
            print("Response: %s" % response.text)
            url_callback_payload = {}
            if response.ok:
                try:
                    response_body = response.json()
                    if response_body['success']:
                        url_callback_payload['status'] = 'finished'
                    else:
                        error_message = response_body['error']['message'].decode('utf-8')
                        print(error_message)
                        url_callback_payload['status'] = 'failed'
                        url_callback_payload['message'] = error_message

                except ValueError:
                    url_callback_payload['status'] = 'failed'
                    print('Response is not a json data')
            else:
                print("Post to `%s` failed." % self.remote_api_url)
                url_callback_payload['status'] = 'failed'
                url_callback_payload['message'] = response.text

            # 采集地址数据回调处理
            response = requests.post('http://localhost:8002/index.php/api/post/url/callback?id=' + str(id), data=url_callback_payload)
            if response.reason == 'Ok':
                response_body = response.json()
                if not response_body['success']:
                    print(response_body['error']['message'].decode('utf-8'))

            else:
                print(response)

            print(80 * '#')
            return item
        else:
            print("Item is invalid.")

    @staticmethod
    def fix_content(html):
        if not html:
            return html

        print("html type is " + str(type(html)))
        pattern = re.compile(r'.*<img.*src=["\'](\S*)["\']\s+')
        images = pattern.findall(html)
        pp = pprint.PrettyPrinter()
        pp.pprint(images)

        for img in images:
            new_img = img
            if img.startswith(('http', '//')):
                url = img
                if img.startswith('//'):
                    url = 'http:' + img
                response = requests.get(url, stream=True)
                if not response.ok:
                    print(response)
                    continue

                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type, False)
                if extension is None:
                    extension = '.png'
                elif extension == '.jpe':
                    extension = '.jpg'

                save_dir = 'D:/tmp'
                path_url = '/uploads/' + datetime.date.today().strftime('%Y%m%d') + '/';
                if not os.path.exists(save_dir + path_url):
                    os.mkdir(save_dir + path_url)

                path_url += uuid.uuid4().__str__() + extension
                new_img = path_url
                f = open(save_dir + path_url, 'wb')

                for block in response.iter_content(1024):
                    if not block:
                        break

                    f.write(block)

                f.close()

                html = html.replace(img, new_img)

        return html
