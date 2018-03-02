# _*_ coding: utf-8 _*_

import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
import time

class DBHelper():
    dbpool = None
    def __init__(self):
        settings = get_project_settings()

        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            cursorclass=pymysql.cursors.DictCursor,
            charset='UTF-8',
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('spider', **db_params)
        self.dbpool = dbpool
        self.cursor = self.connect().cursor


    def connect(self):
        return self.dbpool

    def insert(self, item):
        sql = "INSERT INTO spider(title) VALUES(%s)"
        query = self.dbpool.runInteraction(self._condition_insert(sql, item))

    def _condition_insert(self, tx, sql, item):
        params = {item['title']}
        tx.execute(sql, params)
