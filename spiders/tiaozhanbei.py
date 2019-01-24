# -*- coding: utf-8 -*-
import scrapy
import demjson
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy import Request
import demjson
import json
import time
from matchInfomationSpider.items import MatchinfomationspiderItem
import re
from bs4 import BeautifulSoup
class TiaozhanbeiSpider(scrapy.Spider):
    name = 'tiaozhanbei'
    allowed_domains = ['tiaozhanbei.net']
    url="http://www.tiaozhanbei.net/tzb/notice?page="
    page=1
    start_urls = [url+str(page)]
    #

    def parse(self, response):
        fo = open("test.html", "w")
        # urllist=response.xpath('//div[@class="main wrp"]/div[@class="row mtB"]/div[@class="col-3-4 cont"]/div[@class="funcA mlrB"]/div[@class="pdB"]/ul/li/div/p/a/@href').extract()
        urllist=[]
        soup = BeautifulSoup(response.body.decode('utf-8'), 'lxml')
        # soup.div.div.div.div.div.ul.li.div.p.a['href']
        ulele=soup.find_all('ul')
        index=0
        for uls in ulele:
            if(index==0):
                index=index+1
                continue
            for ul in uls:
                for lis in ul:
                    if(lis.find('a') != -1 and lis.find('a')!=None):
                        urllist.append(lis.find('a')['href'])

        if(self.page < 20):
            self.page=self.page+1
            yield Request(url=self.url + str(self.page), callback=self.parse)
        for item in urllist:
            yield Request(url="http://www.tiaozhanbei.net"+item,callback=self.parse_item)
    def parse_item(self, response):
        soup = BeautifulSoup(response.body.decode('utf-8'), 'lxml')
        title = soup.find_all('h2',attrs={'class':'title taC'})[0]
        contents=response.xpath("//div[@class='lmkdiv']/p/text()").extract()
        contentstring=""
        platform="tiaozhanbei"
        createtimetimeString=response.xpath("//p[@class='txtB taC']/text()").extract()
        #
        temptimeStamp = re.search('\d{4}.(\d{2}|\d{1}).(\d{2}|\d{1})', createtimetimeString[0])
        createtimetimeStamparr=None
        if (temptimeStamp != None):
            createtimetimeStamparr= temptimeStamp.group()
        # createtimetimeArray = time.strptime(createtimestr[0], "%Y-%m-%d")
        # createtimetimeStamp = int(time.mktime(createtimetimeArray))
        createtimetimeStamparr= time.strptime(createtimetimeStamparr, "%Y.%m.%d")
        createtimetimeStamp=int(time.mktime(createtimetimeStamparr))
        item = MatchinfomationspiderItem()
        itemid = re.search('\d+[0-9]', response.url).group()
        for c in contents:
            contentstring=contentstring+c
        contentstring=contentstring+"<br/> detail website url:"+response.url
        # print(title.string)
        # print(contentstring)
        # print(createtimetimeStamparr)
        # print(createtimetimeStamp)

        item['title'] = title.string
        item['content'] = contentstring
        item['createtime'] = createtimetimeStamp
        item['platform'] = platform
        item['itemid'] = itemid
        item['type'] = 0
        yield item