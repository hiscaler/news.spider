# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import mimetypes
import os
import pprint
import re
import uuid

import jieba
import jieba.analyse
import requests
from scrapy.utils.project import get_project_settings


class SogouPipeline(object):
    _api_post_news = None
    _api_post_url = None
    _api_post_attribute = None

    def __init__(self):
        settings = get_project_settings()
        api = settings['BIZ_API']['dev'] if settings['BIZ_DEBUG'] else settings['BIZ_API']['prod']
        self._api_post_news = api['postNews']
        self._api_post_url = api['postUrl']
        self._api_post_attribute = api['postAttribute']

    def process_item(self, item, spider):
        if 'error' in item and item['error']:
            self.post_url_callback(item['post_url_id'], {'status': 'failed'})
        else:
            if item['title'] is not None or item['content'] is not None:
                if 'node_id' not in item or not item['node_id']:
                    item['node_id'] = 884

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
                if 'raw_content' in item and item['raw_content'] is not None:
                    raw_content = item['raw_content']
                    del item['raw_content']
                    raw_text = raw_content.get_text().strip().replace("\n", '')
                    tags = jieba.analyse.extract_tags(raw_text, topK=5, withWeight=True, allowPOS=())
                    tags = set(x for x, y in tags)

                    if tags:
                        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'stopwords.txt')), 'r', encoding='utf-8') as f:
                            stopwords = set(map(lambda s: s.strip(), f.readlines()))
                            if stopwords:
                                tags = set(tags.difference(stopwords))

                        if tags:
                            tags = ','.join(tags)
                            item['keywords'] = tags
                            item['tags'] = tags

                print(80 * '#')
                print(self.__class__.__name__ + '.' + self.process_item.__name__ + ':')
                print(80 * '-')
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(item)

                post_url_id = item['post_url_id']
                del item['post_url_id']

                print('Post to %s' % self._api_post_news)
                response = requests.post(url=self._api_post_news, data=item)
                print("Response: %s" % response.text)
                url_callback_payload = {}
                if response.ok:
                    try:
                        response_body = response.json()
                        if response_body['success']:
                            url_callback_payload['status'] = 'finished'
                            try:
                                # 设置该资讯推送位
                                entity_id = response_body['data']['id']
                                print("Post attribute for #%s" % entity_id)
                                response = requests.post(self._api_post_attribute, {
                                    'entityId': entity_id,
                                    'entityName': 'News',
                                    'alias': 'baidu.bear-pending',
                                })
                                print(response.text)
                                if response.ok:
                                    response_body = response.json()
                                    if not response_body['success']:
                                        print("{id} 设置推送位失败。".format(id=entity_id))

                            except Exception as ex:
                                print(str(ex))
                        else:
                            error_message = response_body['error']['message'].decode('utf-8')
                            print(error_message)
                            url_callback_payload['status'] = 'failed'
                            url_callback_payload['message'] = error_message

                    except ValueError:
                        url_callback_payload['status'] = 'failed'
                        print('Response is not a json data')
                else:
                    print("Post to `%s` failed." % self._api_post_news)
                    url_callback_payload['status'] = 'failed'
                    url_callback_payload['message'] = response.text

                # 采集地址数据回调处理
                self.post_url_callback(post_url_id, url_callback_payload)
                # response = requests.post('http://localhost:8002/index.php/api/post/url/callback?id=' + str(post_url_id), data=url_callback_payload)
                # if response.reason == 'Ok':
                #     response_body = response.json()
                #     if not response_body['success']:
                #         print(response_body['error']['message'].decode('utf-8'))
                #
                # else:
                #     print(response)

                print(80 * '#')
                return item
            else:
                print("Item is invalid.")

    def post_url_callback(self, post_url_id, url_callback_payload):
        response = requests.post(self._api_post_url + '/post/url/callback?id=' + str(post_url_id), data=url_callback_payload)
        if response.reason == 'Ok':
            response_body = response.json()
            if not response_body['success']:
                print(response_body['error']['message'].decode('utf-8'))

        else:
            print(response)

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


if __name__ == '__main__':
    # print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'stopwords.txt')))
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'stopwords.txt')), 'r', encoding='utf-8') as f:
        stopwords = set(map(lambda s: s.strip(), f.readlines()))
        print(stopwords)

    settings = get_project_settings()
    api = settings['BIZ_API']['dev'] if settings['BIZ_DEBUG'] else settings['BIZ_API']['prod']
    print(api)
