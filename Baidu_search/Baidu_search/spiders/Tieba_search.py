#coding:utf-8
'''
Created on 2015/5/7

@author: MINUS
'''
import datetime
import re
import time
import urllib,os

from reportlab.lib.randomtext import subjects
from scrapy import Selector, responsetypes
from scrapy import log, signals
import scrapy
from scrapy.contrib import spiderstate
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Sqlite_DB import SqliteTime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.http.request.form import FormRequest
from scrapy.mail import MailSender
from bs4 import BeautifulSoup
import chardet
from Baidu_search.items import  Topic_Item
import MySQLdb as mdb
from .. import settings

class TiebaSearchSpider(scrapy.Spider):
    name = "Tieba_search"
    # allowed_domains = ["baidu.com"]
    start_urls = (
        'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%BD%BB%B4%F3%D0%A3%C7%EC&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn=2',
    )
    
    def __init__(self, *args, **kwargs):
        super(scrapy.Spider,self).__init__(*args, **kwargs)
        super(TiebaSearchSpider,self).__init__()
        self.dig_pattern = re.compile('(\d+)')
        self.postid_pattern = re.compile('/p/(\d{10})')
        self.page_all=1
        self.site_id=2
        self.site_name = u'tieba_search'
        self.Flag_List = []
        self.Maxpage_List = []
        self.MAX_PAGE_NUM = 5
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Host': 'www.baidu.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        }
    
    def start_requests(self):

        #####################################################################################
        # topic_dict = {'1':[u'考试', u'分数'], '2':[u'北京',u'西安']}
        topic_dict = {'1':[u'萨德'], '2':[u'两会'], '3':[u'西安地铁'], '4':[u'雄安']}
        
        index = 0
        for id, kws_list in topic_dict.iteritems():
            for kw in kws_list:
                print kw
                wd_code = urllib.quote(kw.encode('gbk'))
                search_url = 'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw='+wd_code+'&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1'
                                # http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%B1%B1%BE%A9&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1
                                # http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%B1%B1%BE%A9&un=&rn=10&pn=0&sd=&ed=&sm=1
                # print search_url
                self.Flag_List.append(True)
                self.Maxpage_List.append(self.MAX_PAGE_NUM)
                print search_url
                yield scrapy.Request(search_url,meta={'topic_id': id,'index':index, 'kw':kw},)
                index += 1
        
        #####################################################################################	
        

    def parse(self, response):
        print '___'
        index = response.meta['index']
        topic_id = response.meta[ 'topic_id' ]
        kw = response.meta['kw']
        self.Maxpage_List[index] -= 1
     
        sel = Selector(text=response.body_as_unicode(), type="html")
        all_content = BeautifulSoup(response.body,'html5lib')
        topic_lists = sel.xpath('//div[re:test(@class,"s_post_list")]/div[re:test(@class,"s_post")]')
        print len(topic_lists)
        item_list = []
        for topic in topic_lists:
            topic_item = Topic_Item()
            temp_sel = Selector(text=topic.extract())
            soup = BeautifulSoup(topic.extract(),"lxml")
            
            
            temp_forum = soup.find_all("a",class_="p_forum")
            if len(temp_forum) == 0:
                continue
            
            title = soup.find_all("span",class_="p_title")[0].get_text().strip()
            # print title
            
            post_url = 'http://tieba.baidu.com' + soup.find_all("span",class_="p_title")[0].find('a').get('href').strip()
            # print post_url
            
            temp_font= soup.find_all("font")
            post_time = temp_font[len(temp_font)-1].get_text().strip()+':00'
            # print post_time
            
            forum_name = temp_forum[0].get_text().strip()
            # print forum_name
            author = temp_font[len(temp_font)-2].get_text().strip()
            # print author
            
            content = soup.find_all("div",class_="p_content")[0].get_text().strip()
            # print content
            
            topic_item['topic_id'] = topic_id
            topic_item['topic_url'] = post_url
            # topic_item['topic_content'] = content
            topic_item['topic_pt_time'] = post_time
            topic_item['topic_title'] = title
            topic_item['topic_kw'] = kw
            topic_item['topic_site_id'] = self.site_id
            topic_item['topic_site_name'] = self.site_name
            # topic_item['topic_author'] = author

            item_list.append(topic_item)
        res_items = self.sqldb.get_newest_time(item_list)
        print len(item_list),len(res_items)
        for item in res_items:
            yield scrapy.FormRequest(item['topic_url'],callback=self.parse_torrent,meta={'topic_item':item}) 
            
        if len(item_list) != len(res_items):
            self.Flag_List[index] = False
            
        if self.Flag_List[index] and self.Maxpage_List[index]>0:
            try:
                nextpage_url = 'http://tieba.baidu.com' + all_content.find_all("a", text=u"下一页>")[0].get('href')
            except:
                return
            print nextpage_url
#             raw_input('--')
            yield scrapy.FormRequest(nextpage_url,callback=self.parse,meta={'topic_id': topic_id,'index':index,'kw':kw})

    def parse_torrent(self,response):
        topic_item=response.meta['topic_item']
        scratch_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        topic_item['topic_st_time'] = scratch_time
        
        all_content = BeautifulSoup(response.body,'html5lib')
        answers = all_content.find_all("div",class_="p_content")
        print 'answers len: ', len(answers)
        answer_test = ''
        for answer in answers:
            answer_test += answer.get_text().strip() + u'。'

        topic_item['topic_content'] = answer_test
        print 'got one ________________________'
        yield topic_item
            
    @classmethod
    def from_crawler(cls,crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        crawler.signals.connect(spider.spider_closed,signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider
        
    def spider_closed(self,spider):
        self.sqldb.insert_new_time()
     
    def spider_opened(self,spider):
        self.sqldb = SqliteTime(spider.name)
        

        
