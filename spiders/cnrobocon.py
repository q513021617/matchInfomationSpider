# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy import Request
import demjson
import json
from matchInfomationSpider.items import MatchinfomationspiderItem


class CnroboconSpider(CrawlSpider):
    name = 'cnrobocon'
    allowed_domains = ['api.oversea.edodou.me']
    url='http://api.oversea.edodou.me/v1/notice?title=&page=0&page-size='
    pagsize=1000
    start_urls = [url+str(pagsize)]

    def parse(self, response):
        jsonstr=demjson.decode(response.body)
        datas=jsonstr["data"]
        print(jsonstr["total"])
        print("---------------")

        for jsonindex in datas:

            yield Request(url="http://api.oversea.edodou.me/v1/notice/"+str(jsonindex["token"]), callback=self.parse_item)


    def parse_item(self,response):
        print("----parseItem---")
        #print(response.body)
        item=MatchinfomationspiderItem()
        jsonstr = demjson.decode(response.body)
        title=jsonstr["title"]
        content=jsonstr["content"]
        content=content+"<br/> detail website url:"+response.url
        createtime = jsonstr["created_at"]
        platform = "cnrobocon"
        itemid = jsonstr["token"]
        print(title)

        item['title']=title
        item['content']=content
        item['createtime'] = createtime
        item['platform'] = platform
        item['itemid'] = itemid
        item['type'] = 0
        yield item