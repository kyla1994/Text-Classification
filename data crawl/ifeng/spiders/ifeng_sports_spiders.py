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
    name = "sports"
    start_urls = [
        "http://sports.ifeng.com/listpage/11244/1/list.shtml", #中国足球
        "http://sports.ifeng.com/listpage/31190/1/list.shtml", #中超
        "http://sports.ifeng.com/listpage/35586/1/list.shtml", #亚冠
        "http://sports.ifeng.com/listpage/31186/1/list.shtml",#英超
        "http://sports.ifeng.com/listpage/31188/1/list.shtml", #西甲
        "http://sports.ifeng.com/listpage/31198/1/list.shtml",#欧冠
        "http://sports.ifeng.com/listpage/31419/1/list.shtml",#田径
        "http://sports.ifeng.com/listpage/31418/1/list.shtml",#网球
        "http://sports.ifeng.com/listpage/34120/1/list.shtml",#排球
        "http://sports.ifeng.com/listpage/11246/1/list.shtml",#国际足球
        "http://sports.ifeng.com/listpage/31194/1/list.shtml",#CBA
        "http://sports.ifeng.com/listpage/11247/1/list.shtml",#综合

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
            item['label'] = 'sports'
            if self.check(item['url']):
                yield item
            # //*[@id="pagenext"] //*[@id="pagenext"]
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