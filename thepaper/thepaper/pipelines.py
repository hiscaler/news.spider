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
        use_unicode=False
    )
    return conn


class ThepaperPipeline(object):
    def process_item(self, item, spider):
        print("PROCESS_ITEM .....")
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'insert into thepaper(title, category, summary) values (%s, %s, %s)'

        try:
            cursor.execute(sql, (item['title'], item['category'], item['summary']))
            dbObject.commit()
        except Exception:
            dbObject.rollback()

        return item
