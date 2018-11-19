# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis
from scrapy.exceptions import DropItem


class RedisPipeline(object):
    def open_spider(self, spider):
        self.red = redis.Redis(host='127.0.0.1', password='123456')

    def process_item(self, item, spider):
        if self.red.sadd(spider.name, item['name']):
            print('success')
            return item
        raise DropItem

class QianmuPipeline(object):

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='127.0.0.1',port=3306,db='spider_qianmu',user='root',password='qd970919-',charset='utf8',)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        keys, values = zip(*item.items())
        sql = "insert into `{}` ({}) values ({})".format(
            'qianmu',
            ','.join(keys),
            ','.join(['%s'] * len(values))
        )
        self.cur.execute(sql, values)
        self.conn.commit()
        return item


