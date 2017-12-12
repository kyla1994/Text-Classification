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
    name = "history1"
    start_urls = [
        "http://news.ifeng.com/listpage/71096/1/list.shtml", #假设历史
        "http://news.ifeng.com/listpage/41708/1/list.shtml", #凤凰历史
        "http://news.ifeng.com/listpage/70296/1/list.shtml",#兰台说史
    ]

    def parse(self, response):
        # response.body
        soup = BeautifulSoup(response.body, "lxml")
        #/html/body/div[4]/div[1]/div/div/div[1]/a
        divs = soup.findAll('div', {'class': 'con_lis show'})
        for div in divs:
            # title, content,url
            item = IfengItem()
            url = div.find('a')['href']
            title = div.find('h4').get_text()
            item['url'] = url
            item['title'] = title
            response2 = urllib.urlopen(url)
            soup2 = BeautifulSoup(response2, "lxml")
            content = soup2.find('div', {'id': 'yc_con_txt'}).get_text()
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