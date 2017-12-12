# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from database import Database

class IfengPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def open_spider(self, spider):
        self.database = Database()
        self.database.connect('crawl_data')

    def process_item(self, item, spider):
        try:
            sql = """
               insert into news ( title, content, url, label )
               values (%s,%s,%s,%s)
               """
            data = (item['title'], item['content'], item['url'], item['label'])
            self.database.execute(sql, data)
        except Exception, e:
            print e
            traceback.print_exc()
        return item

    def close_spider(self, spider):
        self.database.close()

