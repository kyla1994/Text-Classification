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
    name = "tech"
    start_urls = [
        "http://tech.ifeng.com/listpage/26344/1/list.shtml", #问题来了
        "http://tech.ifeng.com/listpage/26333/1/list.shtml", #车科技
        "http://tech.ifeng.com/listpage/26335/1/list.shtml", #可穿戴
        "http://tech.ifeng.com/listpage/26334/1/list.shtml",#智慧家庭
        "http://digi.ifeng.com/listpage/4085/1/list.shtml", #手机
        "http://digi.ifeng.com/listpage/11143/1/list.shtml",#苹果
        "http://digi.ifeng.com/listpage/11148/1/list.shtml",#平板
        "http://digi.ifeng.com/listpage/2689/1/list.shtml",#笔记本
        "http://digi.ifeng.com/listpage/5098/1/list.shtml",#影像
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
            item['label'] = 'technology'
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