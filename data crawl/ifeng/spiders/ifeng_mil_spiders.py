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
    name = "mil"
    start_urls = [
        "http://news.ifeng.com/listpage/7130/1/list.shtml", #环球军情
        "http://news.ifeng.com/listpage/7131/1/list.shtml",#防务观察
        "http://news.ifeng.com/listpage/7111/1/list.shtml",#资料库
    ]

    def parse(self, response):
        #response.body
        soup = BeautifulSoup(response.body ,"lxml")
        divs = soup.findAll('div',{'class':'comListBox'})
        for div in divs:
            #title, content,url
            item = IfengItem()
            h2 = div.find('h2')
            link = h2.find('a')
            url = link['href']
            item['url'] = url
            title = link.get_text()
            item['title'] = title
            response2 = urllib.urlopen(url)
            soup2 = BeautifulSoup(response2, "lxml")
            content = soup2.find('div',{'id':'main_content'}).get_text()
            item['content'] = content
            item['label'] = 'military'
            if self.check(item['url']):
                yield item

            next_url = response.xpath("//div[@class='m_page']/a[@id='pagenext']/@href").extract()  # 找到下一个链接，也就是翻页。

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