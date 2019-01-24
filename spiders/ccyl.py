# -*- coding: utf-8 -*-
import scrapy
from matchInfomationSpider.items import MatchinfomationspiderItem
from scrapy import Request
from bs4 import BeautifulSoup
import time
class CcylSpider(scrapy.Spider):
    name = 'ccyl'
    allowed_domains = ['ccyl.org.cn']
    url="http://www.gqt.org.cn/notice/"
    page=1
    start_urls = ["http://www.gqt.org.cn/notice/index.htm"]


    def urlfull(self,url):
        if(url[0:2]=='..'):
            print('..')
            if(url[-4:]=='.htm'):
                return("http://www.gqt.org.cn/"+url[3:])
            if (url[-4:] == '.pdf'):
                return("http://www.gqt.org.cn/" + url[3:])
            if (url[-5:] == '.html'):
                return("http://www.gqt.org.cn/"+url[3:])
            print("http://www.gqt.org.cn/" + url[3:])
            return "http://www.gqt.org.cn/" + url[3:]
        if (url[0:2] == './'):
            print('.')
            if (url[-4:] == '.htm'):
                print("htm")
            if (url[-4:] == '.pdf'):
                print("pdf")
            if (url[-5:] == '.html'):
                print("html")
            print("http://www.gqt.org.cn/" + url[2:])
            return "http://www.gqt.org.cn/" + url[2:]
        if (url[0:2] != '..'):
            print('html')

            print(url)
            return url
    def parse(self, response):
        #
        # //ul['rdwz']/li/a/@href
        urllist=response.xpath("//ul['rdwz']/li/a/@href").extract()
        titlist=response.xpath("//ul['rdwz']/li/a/text()").extract()
        timelist=response.xpath("//ul['rdwz']/li/font/text()").extract()



        tempitem=MatchinfomationspiderItem()
        tempitemList=[]
        if (self.page < 20):
            self.page = self.page + 1
            yield Request(url=self.url + "index_" + str(self.page - 1) + ".html", callback=self.parse)
        # print(urllist)
        for index in range(len(urllist)):
            tempitem['content']=self.urlfull(urllist[index])
            tempitem['title']=titlist[index]
            if(index>49):
                break
            createtimetimeStamparr = time.strptime(timelist[index], "%Y-%m-%d %H:%M:%S")

            createtimetimeStamp = int(time.mktime(createtimetimeStamparr))
            tempitem['createtime']=createtimetimeStamp
            tempitem['platform']="ccyl"
            tempitem['itemid']=0
            tempitem['type']=0
            if (tempitem['content'][-4:] == '.htm' or tempitem['content'][-4:] == '.html'):
                # print("htm")
                yield Request(url=tempitem['content'],callback=self.parse_item)
            if (tempitem['content'][-4:] == '.pdf'):
                yield tempitem

            print(tempitem['title'])
            print(tempitem['content'])
            print(createtimetimeStamp)

    def parse_item(self,response):
        print(response.body)