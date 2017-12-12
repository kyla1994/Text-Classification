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
    name = "politics"
    start_urls = [
        "http://news.qq.com/newsgn/zhxw/shizhengxinwen.htm", #时政
    ]
    #
    base = "http://news.qq.com/newsgn/zhxw/shizhengxinwen_"#80.htm
    for i in range(2,81):
        url = base +str(i)+".htm"
        start_urls.append(url)
    def parse(self, response):
        # response.body
        soup = BeautifulSoup(response.body, "lxml")
        root = soup.find('div',{'class':'mod newslist'})
        lis = root.findAll('li')
        for li in lis:
            # title, content,url
            item = IfengItem()
            url = li.find('a')['href']
            item['url'] = url
            title = li.get_text()
            item['title'] = title
            response2 = urllib.urlopen(url)
            soup2 = BeautifulSoup(response2, "lxml")
            try:
                content = soup2.find('div', {'class': 'main'}).get_text()
            except AttributeError:
                print AttributeError.message

            item['content'] = content
            item['label'] = 'politics'
            if self.check(item['url']):
                yield item

            # next_url = response.xpath("//*[@class='f12'] /@href").extract()  # 找到下一个链接，也就是翻页。
            #
            # if next_url:
            #     yield scrapy.Request(next_url[0], callback=self.parse)

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