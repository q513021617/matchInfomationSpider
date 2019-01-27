# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy import Request
import demjson
import json
import time
from matchInfomationSpider.items import MatchinfomationspiderItem
import re
from bs4 import BeautifulSoup


class RobocupSpider(scrapy.Spider):
    name = 'robocup'
    allowed_domains = ['robocup.org']
    start_urls = ['https://www.robocup.org/events/upcoming_events']

    def parse(self, response):
        urllist=response.xpath("//h4/a/@href").extract()
        for url in urllist:
            yield Request(url="https://www.robocup.org"+url,callback=self.parse_item)
    def parse_item(self,response):
        content=response.xpath("//div[@class='gdlr-blog-content']").extract()
        contentstr=""
        item = MatchinfomationspiderItem()
        titlestr=response.xpath("//h1/text()").extract()
        for cu in content:
            contentstr=contentstr+cu
        contentstr=contentstr+"<br/> detail website url:"+response.url
        itemid = re.search('\d+[0-9]', response.url).group()
        platform="robocup"
        print(titlestr[0])
        print(itemid)
        item['title'] = titlestr[0]
        item['content'] = contentstr
        item['createtime'] = 0
        item['platform'] = platform
        item['itemid'] = itemid
        item['type'] = 0
        yield item