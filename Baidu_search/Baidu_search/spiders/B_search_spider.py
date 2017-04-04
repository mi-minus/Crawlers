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

from Baidu_search.items import  Topic_Item
import MySQLdb as mdb
from .. import settings

class DmozSpider_search(CrawlSpider):
    name = "baidu_search"
#     allowed_domains = ["baidu.com"]
    
    def start_requests(self):
        db = mdb.connect(host = settings.DB_HOST, user = settings.DB_NAME, passwd = settings.DB_PASSWD,db = settings.DB,charset="utf8" )
        cur=db.cursor()
        cur.execute('select topic_id,topic_keywords from topic where topic_id in (select topic_id from site_topic where site_id=%d)' % self.site_id)
        topic_kws = cur.fetchall()	
		#####################################################################################
        now = time.strftime('%Y%m%d', time.localtime())
        cur.execute('show tables from yq like "post_%s"' % str(now))
        db.commit()
        tables = cur.fetchone()
        cur.close()
        db.close()
        print tables
        # raw_input(':::')
        if tables == None or len(tables)==0:
            os.system("python D:/crawler/create_db.py %s"%('post_' + now))
        table_name = 'post_' + now
        #####################################################################################	
        index = 0
        print topic_kws
        for topic_kw in topic_kws:
            topic_id = topic_kw[0]
            kws = topic_kw[1]
            kws_list = kws.split(',')
            for kw in kws_list:
                wd_code = urllib.quote(kw.encode('utf-8'))

                search_url = 'http://www.baidu.com/s?wd='+wd_code+'&pn=0&tn=baidurt&ie=utf-8&rtt=4&bsst=1'
                print search_url + 'mmmmmmmmmmmmmmmmmmm'
                self.Flag_List.append(True)
                self.Maxpage_List.append(self.MAX_PAGE_NUM)                    
                yield scrapy.FormRequest(search_url,meta={'topic_id': topic_id,'index':index,'table_name':table_name},headers=self.headers)
                index += 1           
#                    
    def __init__(self, *args, **kwargs):
        super(scrapy.Spider,self).__init__(*args, **kwargs)
        # self.sqldb = SqliteTime(self.name)        
        super(DmozSpider_search,self).__init__()
        self.dig_pattern = re.compile('(\d+)')
        self.postid_pattern = re.compile('/p/(\d{10})')
        self.page_all=1
        self.site_id = 500
        self.Flag_List = []
        self.Maxpage_List = [] 
        self.MAX_PAGE_NUM = 5        
        self.headers={
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Language' : 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                      'Connection' : 'keep-alive',
                      'DNT' : '1',
                      'Host' : 'www.baidu.com',
                      'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                      }
        self.content_pa1=re.compile('</div>(.*?)<br',re.S)
    
    def parse_html_content(self,str):
        sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)
        str = re.sub(sub_p_1, '', str)    
        ustr = str
        return ustr
    
    def tranun(self,s):
        l=len(s)
        ss=''
        i=0
        while i<l:
            if s[i]=='\\' and s[i+1]=='u':
                ss=ss+unichr(int(s[i+2:i+6],16))
                i=i+6
            else:
                ss=ss+s[i]
                i+=1
        return ss
    
    def parse(self,response):
    
        index = response.meta['index']
        topic_id = response.meta[ 'topic_id' ]
        self.Maxpage_List[index] -= 1    
        table_name = response.meta['table_name']
        sel = Selector(text=response.body, type="html")
       
        topic_lists = sel.xpath('//table[re:test(@class,"result")]')
        all_content = BeautifulSoup(response.body,'html5lib')
        item_list = []
        for topic in topic_lists:
            topic_item = Topic_Item()
            temp_sel = Selector(text=topic.extract())
            soup = BeautifulSoup(topic.extract())
            topic_item['topic_id'] = topic_id
            
            
            ####################################################################################
            post_time=''
            now = datetime.datetime.now()
            dig_pa = re.compile(r'(.*?)\\xa0-\\xa(\d+)(.*?)\Z')
            dig_pa_ = re.compile(r'u\'(\d*)')
            poster_time = temp_sel.xpath('//div[re:test(@class,"realtime")]/text()').extract()[0]
            con = poster_time.__repr__()
            # print con
            try:
                three_parts = re.findall(dig_pa,con)[0]
                from_source = three_parts[0][2:]
                author = self.tranun(from_source)
                
                time_dig = int(three_parts[1])
    
                if '5929' in three_parts[2]:
                    print 'day'
                    new_time = now - datetime.timedelta(days=time_dig)
                    
                elif '5c0f' in three_parts[2]:
                    print 'xiao shi'
                    new_time = now - datetime.timedelta(hours=time_dig)
                    
                elif '5206' in three_parts[2]:
                    print 'fenzhong'   
                    new_time = now - datetime.timedelta(minutes=time_dig)
            except:
                author = ''
                time_dig = int(re.findall(dig_pa_, con)[0])

                if '5929' in con:
                    print 'day'
                    new_time = now - datetime.timedelta(days=time_dig)
                    
                elif '5c0f' in con:
                    print 'xiao shi'
                    new_time = now - datetime.timedelta(hours=time_dig)
                    
                elif '5206' in con:
                    print 'fenzhong'   
                    new_time = now - datetime.timedelta(minutes=time_dig)                
                print '++++++++++++++++++++++'
            
          
            topic_item['topic_post_time']= new_time.strftime('%Y-%m-%d %H:%M:%S')  
            topic_item['topic_author'] = author
            ####################################################################################
#             title = temp_sel.xpath('//h3[re:test(@class,"t")]/a/text()').extract()[0]
#             print title + ' titile>>>'
            
            topic_title = soup.find_all('h3',class_='t')[0].get_text()
            topic_item['topic_title'] = topic_title
            ####################################################################################
#             content = temp_sel.xpath('//td[re:test(@class,"f")]//font[re:test(@size,"-1")]/text()').extract()[0]
#             print content +' >>>><'
#             topic_item['topic_content'] = content

            content_all = soup.find_all('font',attrs={'size':'-1'})[0].get_text()
            topic_item['topic_content'] = content_all
            ####################################################################################
            ####################################################################################
            url = temp_sel.xpath('//h3[re:test(@class,"t")]/a/@href').extract()[0]
            print 'url:'+url
            topic_item['topic_url']=url
            topic_item['table_name'] = table_name
            
            item_list.append(topic_item)
        res_items = self.sqldb.get_newest_time(item_list)
        for item in res_items:
            yield scrapy.Request(item['topic_url'],callback=self.parse_torrent,meta={'topic_item':item},headers=self.headers) 
        if len(item_list) != len(res_items):
            self.Flag_List[index] = False  
            
        if self.Flag_List[index] and self.Maxpage_List[index]>0:
            try:
                nextpage_url = 'http://www.baidu.com/' + all_content.find_all("a", text=u"下一页>")[0].get('href')
            except :
                return
            print nextpage_url
            yield scrapy.Request(nextpage_url,callback=self.parse,meta={'index':index,'topic_id': topic_id,'table_name':table_name},headers=self.headers) 
            
    def parse_torrent(self,response):    
        topic_item=response.meta['topic_item']
        scratch_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        topic_item['scratch_time'] = scratch_time        
        topic_item['topic_board']='百度搜一搜'
        topic_item['site_id']=self.site_id
        topic_item['data_type']=5
        
        topic_item['thread_content'] = response.body
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
