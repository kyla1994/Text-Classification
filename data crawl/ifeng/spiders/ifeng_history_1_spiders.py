#coding=utf-8
import scrapy
from ifeng.items import IfengItem
import datetime
import urllib2
import hashlib
import urllib
from bs4 import BeautifulSoup
from ifeng.database import Database

import traceback
import scrapy
from ..items import IfengItem
import datetime
import time
import urllib2
import json
import hashlib
import random
from ..database import Database
from scrapy import Selector
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')
class IfengSpider(scrapy.Spider):
    name = "history"
    start_urls = [
        "http://news.ifeng.com/listpage/4765/1/list.shtml", #世界史
        "http://news.ifeng.com/listpage/4764/1/list.shtml", #中国古代史
        "http://news.ifeng.com/listpage/4763/1/list.shtml",#中国近代史
        "http://news.ifeng.com/listpage/4762/1/list.shtml",#中国现代史
    ]

    def parse(self, response):
        # response.body
        soup = BeautifulSoup(response.body, "lxml")
        divs = soup.findAll('div', {'class': 'box_list clearfix'})
        for div in divs:
            # title, content,url
            item = IfengItem()
            h2 = div.find('h2')
            link = h2.find('a')
            url = link['href']
            item['url'] = url
            title = link['title']
            item['title'] = title
            response2 = urllib.urlopen(url)
            soup2 = BeautifulSoup(response2, "lxml")
            content = soup2.find('div', {'id': 'artical_real'}).get_text()
            item['content'] = content
            item['label'] = 'history'
            if self.check(item['url']):
                yield item
             #//*[@id="pagenext"]
            next_url = response.xpath("//*[@id='pagenext'] /@href").extract()  # 找到下一个链接，也就是翻页。

            if next_url:
                yield scrapy.Request(next_url[0], callback=self.parse)
    def check(self, url):
        self.database = Database()
        self.database.connect('crawl_data')
        sql = "SELECT * FROM news where url=%s order by url"
        str_article_url = url.encode('utf-8')
        data = (str_article_url,)
        try:
            search_result = self.database.query(sql, data)
            if search_result == ():
                self.database.close()
                return True

        except Exception, e:
            print e
            traceback.print_exc()
        self.database.close()
        return False