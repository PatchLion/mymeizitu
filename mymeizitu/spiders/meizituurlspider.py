# -*- coding: utf-8 -*-
import scrapy

import redis

from mymeizitu.spiders import DEFAULT_REDIS_KEY
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy import Selector


#'myspider:start_urls'
class MeizituUrlSpider(Spider):
    name = "meizituurl"
    allowed_domains = ["meizitu.com"]
    start_urls = ['http://meizitu.com/']
    _redis_instance = redis.Redis(password='123')

    def parse(self, response):
        #print("url->", str(response.url))
        sel = Selector(response)
        urls = sel.xpath("//div[@class='tags']/span/a/@href").extract()
        for url in set(urls):
            yield Request(url, callback=self.parse_childpage)

    def parse_childpage(self, response):
        print("child_page_url:", str(response.url))
        #解析子项url
        sel = Selector(response)
        urls = sel.xpath("//ul[@class='wp-list clearfix']/li/div[@class='con']/h3[@class='tit']/a/@href").extract()
        for url in set(urls):
            self._redis_instance.lpush(DEFAULT_REDIS_KEY, url)

        #下一页
        nexthtml = sel.xpath("//div[@id='wp_page_numbers']/ul/li/a[text()='下一页']/@href").extract()
        if len(nexthtml) > 0:
            nexturl = 'http://meizitu.com/a/' + nexthtml[0]
            return Request(nexturl, callback=self.parse_childpage)