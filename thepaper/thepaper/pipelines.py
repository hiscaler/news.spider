# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


def dbHandle():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        db='spider',
        passwd='root',
        charset='utf8',
        use_unicode=True
    )
    return conn


class ThepaperPipeline(object):
    def process_item(self, item, spider):
        print("PROCESS_ITEM .....")
        db_handle = dbHandle()
        cursor = db_handle.cursor()
        cursor.execute('SELECT COUNT(*) FROM thepaper WHERE url = "' + item['url'] + '"')
        data = cursor.fetchone()
        print("-------------")
        if data[0]:
            print("Query is exist")
        else:
            print('Query is none')
            db_handle.begin()
            try:
                sql = 'INSERT INTO thepaper(url, title, category, summary, content) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(sql, (item['url'], item['title'], item['category'], item['summary'], item['content']))
                db_handle.commit()
            except Exception as err:
                print(err)
                db_handle.rollback()
            finally:
                db_handle.close()

        return item
