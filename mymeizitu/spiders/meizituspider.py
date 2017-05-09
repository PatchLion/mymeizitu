# -*- coding: utf-8 -*-
import scrapy
import redis
import os

from mymeizitu.spiders import DEFAULT_REDIS_KEY
from scrapy_redis.spiders import RedisSpider
from scrapy import Selector
from mymeizitu.items import MymeizituItem




class MeizituSpider(RedisSpider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    #start_urls = ['http://meizitu.com/']
    redis_key = DEFAULT_REDIS_KEY

    def __init__(self):
        super(RedisSpider, self).__init__()


    def parse(self, response):
        print("url->", str(response.url))
        sel = Selector(response)
        item = MymeizituItem()
        item["title"] = sel.xpath("//div[@class='metaRight']/h2/a/text()").extract()[0]
        item["imageurls"] = sel.xpath("//p/img/@src").extract()
        item["url"] = str(response.url)
        return item
