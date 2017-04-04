# -*- coding: utf-8 -*-
import scrapy
from .. import settings

import time
from scrapy import signals
from baiduweibo.items import Topic_Item
from scrapy.selector import Selector
import re
import chardet
import urllib
from bs4 import BeautifulSoup 
import datetime
# from mongoengine import *
import sys
# from baiduweibo.Sqlite_DB import SqliteTime
# from .. import models

# reload(sys)
# sys.setdefaultencoding('utf-8')

# conn = connect('yuqing', alias='default', host='117.32.155.62', port=10005, username='yuqing', password='yuqing')


class BaiduweiboSpider(scrapy.Spider):
    name = 'baidu_weibo'
    allowed_domains = []
    start_urls = []

    def __init__(self,*args,**kwargs):
        super(scrapy.Spider,self).__init__(*args,**kwargs)
        self.Flag_List = []
        self.Maxpage_List = []
        self.MAX_PAGE_NUM = 76
        self.site_id =  1   #微博站点号
        self.site_name = u'baidu_weibo'
        self.base_url = 'https://www.baidu.com/s?wd=%s&pn=0&cl=2&tn=baiduwb&ie=utf-8&f=3&rtt=2'
        self.topic_kws = None
        self.pa = re.compile('&pn=(\d+)&') 
        self.pa_time = re.compile('\d+')
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Host': 'www.baidu.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        
        self.headers_weibo = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Host': 'weibo.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
        }

    def start_requests(self):
        # topic_dict = {'1':[u'萨德'], '2':[u'两会'], '3':[u'西安地铁']}
        topic_dict = {'1':[u'萨德'], '2':[u'两会'], '3':[u'西安地铁'], '4':[u'雄安']}
        
        ind = 0
        for id, kws_list in topic_dict.iteritems():
            for kw in kws_list:
                self.Flag_List.append(True)
                self.Maxpage_List.append(self.MAX_PAGE_NUM)
                quote_kw = urllib.quote(kw.encode('utf-8'))
                url = self.base_url % quote_kw
                print url, ind, id

                yield scrapy.Request(url,meta={'index':ind, 'topic_id': id, 'kw':kw},headers=self.headers)
                ind += 1

        # print self.Maxpage_List
        # print self.Flag_List

    def parse(self,response):
        index = response.meta['index']
        topic_id = response.meta['topic_id']
        kw = response.meta['kw']

        all_content = BeautifulSoup(response.body,'html5lib')
        self.Maxpage_List[index] -= 1

        news_list = all_content.select('#weibo > li')
        print "next_list" ,len(news_list)
        # return 
        
        for new in news_list:
            print '+'
            url_title_1 = ''
            
            url = new.find_all('a',class_='weibo_all')[0].get('href')
            # url = new.xpath('div//a[@class="weibo_all"]/@href').extract()[0]
            print url
            
            post_time = new.find_all('div', class_='m')[0].get_text().strip().encode('utf-8')
            # post_time = new.xpath('//div[@class="m"]/a/text()').extract()[0]
            if '小时' in post_time:
                # with open('d:/1.txt','a+') as f:
                    # f.write(post_time)
                    # f.write('\r\n')
                digit_hour = re.findall(self.pa_time, post_time)[0]
                post_time = (datetime.datetime.now() - datetime.timedelta(hours = int(digit_hour))).strftime("%Y-%m-%d %H:%M:%S")
                print post_time
            else:
                continue
            
            #评论
            # reply_num = new.xpath('div/div/div/a[@name="weibo_ping"]/text()').extract()[0]
            # real_reply = reply_num[reply_num.index('(')+1:reply_num.index(')')]
            # 转发
            # read_num = new.xpath('div/div/div/a[@name="weibo_trans"]/text()').extract()[0]
            # real_read = read_num[read_num.index('(')+1:read_num.index(')')]

            # print real_reply,real_read

            # poster = new.xpath('div[2]/p/a[1]/text()').extract()[0]
            # poster_url = new.xpath('div[2]/p/a[1]/@href').extract()[0]
            # poster_id = new.xpath('')

            content = new.select('.weibo_detail > p')[0].get_text()
            # with open('d:/1.txt','a+') as f:
                # f.write(con)
                # f.write('\r\n')
            # print con
            # return

            topic_item = Topic_Item()
            topic_item['topic_id'] = topic_id
            topic_item['topic_url'] = url
            topic_item['topic_content'] = content
            topic_item['topic_pt_time'] = post_time
            topic_item['topic_title'] = ''
            topic_item['topic_kw'] = kw
            topic_item['topic_site_id'] = self.site_id
            topic_item['topic_site_name'] = self.site_name
            scratch_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            topic_item['topic_st_time'] = scratch_time

            print '-=-=-=-='
            yield topic_item
            # yield scrapy.Request('http://weibo.com/2060127212/EzRaulRNw',callback=self.parse_news,meta={'topic_item':topic_item}, headers = self.headers_weibo)
            # return
            
        if self.Flag_List[index] and self.Maxpage_List[index] > 0:
            page_ind = (self.MAX_PAGE_NUM - self.Maxpage_List[index]) * 10
            next_url = re.sub(self.pa, '&pn='+str(page_ind)+'&', response.url)
            yield scrapy.Request(next_url, meta={'index':index, 'topic_id': topic_id,'kw':kw},headers=self.headers)

    def parse_news(self, response):
        print '============='
        print response.body
        topic_item = response.meta['topic_item']
        # newsitem['topic_thread_content'] = response.body
        # newsitem['site_id'] = self.site_id
        # newsitem['data_type'] = 2
        
        # return newsitem















