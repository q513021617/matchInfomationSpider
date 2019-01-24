# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
from pymysql import cursors

class MatchinfomationspiderPipeline(object):
    cursor=None
    def __init__(self):

        conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="root",db="matchInfomation",charset="utf8")
        conn.autocommit(True)  # 设置自动commit
        self.cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 设置返回的结果集用字典来表示，默认是元祖
    def process_item(self, item, spider):
        print("-----Pipeline------")
        print(item["title"])
        print(item["createtime"])

        self.cursor.execute("insert into notify(title,content,createtime,platform,itemid,type) values('"+item["title"]+"','"+item["content"]+"',"+str(item["createtime"])+",'"+item["platform"]+"',"+str(item["itemid"])+","+str(item["type"])+")")
        return item
