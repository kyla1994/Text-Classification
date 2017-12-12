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
    name = "ifeng"
    start_urls = []
    bases = [
        "http://ent.ifeng.com/listpage/3/", #明星
        "http://ent.ifeng.com/listpage/30741/",#演出
        "http://ent.ifeng.com/listpage/1370/",#电视
        "http://ent.ifeng.com/listpage/6/", #电影
        "http://ent.ifeng.com/listpage/30282/",#明星抓取
        "http://ent.ifeng.com/listpage/44168/",#电视新闻
        "http://ent.ifeng.com/listpage/44169/",#影视新闻
    ]
    for base in bases:
        for i in xrange(1,21):
            url = base + str(i) + '/list.shtml'
            start_urls.append(url)

    def parse(self, response):
        #response.body
        soup = BeautifulSoup(response.body ,"lxml")
        divs = soup.findAll('div',{'class':'box_list clearfix'})
        for div in divs:
            #title, content,url
            item = IfengItem()
            h2 = div.find('h2')
            link = h2.find('a')
            url = link['href']
            item['url'] = url
            title = link['title']
            item['title'] = title
            response2 = urllib.urlopen(url)
            soup2 = BeautifulSoup(response2, "lxml")
            content = soup2.find('div',{'id':'artical_real'}).get_text()
            item['content'] = content
            item['label'] = 'entertainment'
            if self.check(item['url']):
                yield item
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