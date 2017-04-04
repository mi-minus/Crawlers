# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from weibo_pc.items import WeiboPcItem
from scrapy.conf import settings
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
from scrapy import log
import settings
import os 
import urllib
from urllib import urlopen
import urllib2
import requests


class WeiboPcPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                                    dbapiName = 'MySQLdb',
                                    host = 'localhost',
                                    db = 'sina_spider_db',
                                    user = 'root',
                                    passwd = 'gongli',
                                    cursorclass = MySQLdb.cursors.DictCursor,
                                    charset = 'utf8mb4',
                                    )

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self._conditional_insert,item)
        return item

    def _conditional_insert(self,tx,item):
        query = u"INSERT INTO test_table_3 (u_name , u_id , u_content ,u_time) values (%s , %s , %s , %s)"

        param = (item['user_name'] , item['user_id'] , item['blog_content'] , item['report_time'])
        
        tx.execute(query,param)
