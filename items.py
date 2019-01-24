# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchinfomationspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content =scrapy.Field()
    createtime=scrapy.Field()
    platform=scrapy.Field()
    itemid=scrapy.Field()
    # 0 通知 1 新闻
    type=scrapy.Field()