# encoding=utf-8
import re
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
import random
import scrapy 
import os 
import urllib
import urllib2
from bs4 import BeautifulSoup
from lxml import etree
from weibo_pc.transtoHTML import transtoHtml,TranstoHtml
from weibo_pc.items import WeiboPcItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#12.11 night
#浏览器HEAD不同会造成获取到的页面格式不同导致不能用同样的方法解析。
#
class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        for day in range(2,3):
            for hour in range(0,24):
                url = "http://s.weibo.com/weibo/%25E8%2580%2583%25E7%25A0%2594&typeall=1&suball=1&\
                    timescope=custom:2017-1-{}-{}:2017-1-{}-{}&page=1".format(day,hour,day,hour)
                yield Request(url , callback=self.parse)
        # url = 'http://s.weibo.com/weibo/%25E8%2580%2583%25E7%25A0%2594&typeall=1&suball=1&timescope=custom:2017-01-02:2017-01-03&Refer=g'
        # yield Request(url, callback=self.parse)


    def parse(self,response):
        page_content = response.body
        selector = etree.HTML(page_content)

        meta_script = selector.xpath('//script/text()')
        print len(meta_script)

        for script in meta_script:
            
            item = WeiboPcItem()
            tostring = str(script)
            real_content = transtoHtml(tostring)

            if real_content =='error' or '':
                print 'Error Occurred'
                continue
            else:
                real_content_str = str(real_content[0]).decode("string_escape")
                final_content = real_content_str.replace('\/','/')

                sel = etree.HTML(final_content)

                for grid in sel.xpath('//div[@class="content clearfix"]'):
                    #用户名
                    uname = grid.xpath('div[1]/a[1]/text()')
                    item['user_name'] = ('').join(uname)
                    #微博内容
                    bcontent = grid.xpath('div[1]/p[@node-type="feed_list_content_full"]//text()')
                    if bcontent:
                        item['blog_content'] = ('').join(bcontent)
                    else:
                        bcontent_another = grid.xpath('div[1]/p[@class="comment_txt"]//text()')
                        item['blog_content'] = ('').join(bcontent_another)
                    #用户ID，来追踪主页
                    user_id = grid.xpath('div[1]/a[1]/@usercard')
                    print user_id
                    uid = user_id[0]
                    item['user_id'] = uid[(uid.index("id=")+3):(uid.index("usercardkey")-2)]

                    #时间信息，分析时间
                    rtime = grid.xpath('div[2]/a[1]/@title')
                    item['report_time'] = ('').join(rtime)

                    next_page = grid.xpath('//a[@class="page next S_txt1 S_line1"]/@href')
                    
                    try:
                        all_addr = item['blog_content'].index('\\u5c55\\u5f00\\u5168\\u6587')
                        full_content_page_url = grid.xpath('div[@class="feed_from W_textb"]/a[1]/@href')[0]
                        print full_content_page_url
                        wap_web = full_content_page_url.replace('com','cn')
                        print '1111'
                        yield Request(wap_web,callback=self.parse_allcontent, meta={'item':item})
                    except:
                        print '2222'
                        yield item
                        pass

                # next_page = grid.xpath('//a[@class="page next S_txt1 S_line1"]/@href')

                if next_page:
                    next_url = 'http://s.weibo.com' + next_page[0]
                    
                    yield Request(next_url,callback=self.parse)



    def parse_allcontent(self,response):

        item_callback = response.meta['item']
        items = WeiboPcItem()
        lxml_etree = response.body
        sel = etree.HTML(lxml_etree)
        uname = sel.xpath('//div[@id="M_"]/div/a/text()')[0]
        items['user_name'] = uname
        bcontent = sel.xpath('//div[@id="M_"]/div[1]/span[@class="ctt"]//text()')
        real_bcontent = ''.join(bcontent)

        items['blog_content'] = real_bcontent
        items['user_id'] = item_callback['user_id']
        items['report_time'] = item_callback['report_time']
        yield items














    # def ItemGet(self,content):
    #     print '222222'
    #     sel = etree.HTML(content)

    #     for grid in sel.xpath('//div[@class="content clearfix"]'):
    #         #用户名
    #         item['user_name'] = grid.xpath('div[1]/a[1]/text()')   
    #         #微博内容
    #         item['blog_content'] = grid.xpath('div[1]/p[@class="comment_txt"]//text()')
    #         #用户ID，来追踪主页
    #         user_id = grid.xpath('div[1]/a[1]/@usercard')
    #         print user_id
    #         uid = user_id[0]
    #         item['user_id'] = uid[(uid.index("id=")+3):(uid.index("usercardkey")-2)]

    #         #时间信息，分析时间
    #         item['report_time'] = grid.xpath('div[2]/a[1]/@title')

    #         yield item

    #     next_page = grid.xpath('//a[@class="page next S_txt1 S_line1"]/@href')
    #     if next_page[0]:
    #         next_url = 'http://s.weibo.com' + next_page[0]
    #         raw_input()
    #         yield Request(next_url,callback=self.parse)


                # for grid in sel.xpath('//div[@class="content clearfix"]'):
                #     #用户名
                #     item['user_name'] = grid.xpath('div[1]/a[1]/text()')   
                #     #微博内容
                #     item['blog_content'] = grid.xpath('div[1]/p[@class="comment_txt"]//text()')
                #     #用户ID，来追踪主页
                #     user_id = grid.xpath('div[1]/a[1]/@usercard')
                #     print user_id
                #     uid = user_id[0]
                #     item['user_id'] = uid[(uid.index("id=")+3):(uid.index("usercardkey")-2)]

                #     #时间信息，分析时间
                #     item['report_time'] = grid.xpath('div[2]/a[1]/@title')

                #     next_page = grid.xpath('//a[@class="page next S_txt1 S_line1"]/@href')
                #     yield item