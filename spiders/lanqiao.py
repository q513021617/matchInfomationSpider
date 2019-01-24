# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy import Request
import demjson
import json
import time
from matchInfomationSpider.items import MatchinfomationspiderItem
import re
class LanqiaoSpider(scrapy.Spider):
    name = 'lanqiao'
    allowed_domains = ['lanqiao.org']
    # http://www.lanqiao.org/?c=mobile&m=newslist&type=20&p=2
    url="http://www.lanqiao.org/?c=mobile&m=newslist&type=20&p="
    page=1
    start_urls = [url+str(page)]

    def parse(self, response):

        jsonstringdata = demjson.decode(response.body)
        datastring = jsonstringdata["data"]
        for jsonindex in datastring:
            yield Request(url="http://www.lanqiao.org/?c=mobile&m=newsdetail&id="+str(jsonindex['id']), callback=self.parse_item)
        if(self.page<20):
            self.page+=1
            yield Request(url=self.url+str(self.page), callback=self.parse)

    def parse_item(self, response):
        print("----parseItem---")
        # print(response.body)
        item = MatchinfomationspiderItem()
        # jsonstr = demjson.decode(response.body)
        # //div[@class='title']
        title = response.xpath("//div[@class='title']/text()").extract()
        #//div[@class='content']//p//span/text()
        contentarr = response.xpath("//div[@class='content']//p//span/text()").extract()
        content=""
        for stritem in contentarr:
            content=stritem+content
        content=content+"<br/> detail website url:"+response.url
        #//div[@class="source"]/span/text()
        createtimestr = response.xpath("//div[@class='source']/span/text()").extract()

        createtimetimeArray = time.strptime(createtimestr[0], "%Y-%m-%d")
        createtimetimeStamp = int(time.mktime(createtimetimeArray))
        platform = "lanqiao"
        itemid = re.search('\d+[0-9]',response.url).group()
        # print(title)
        # print(createtimetimeStamp)
        # print(content)
        # print(response.url)
        # print(itemid)
        item['title'] = title[0]
        item['content'] = content
        item['createtime'] = createtimetimeStamp
        item['platform'] = platform
        item['itemid'] = itemid
        item['type'] = 0
        yield item