#coding:utf-8
import os
os.chdir('C:/Users/MINUS/Desktop/ALL/yq_minus/baidu_micro_blog/baiduweibo')

from scrapy import log
from scrapy.crawler import Crawler,CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings

# from Baidu_search.spiders.B_search_spider import DmozSpider_search

# spider = DmozSpider_search()
# settings = get_project_settings()
# crawler = Crawler(settings)
# crawler.configure()
# crawler.crawl(spider)
# crawler.start()

# log.start()
# reactor.run()

settings = get_project_settings()
############################################################################
spname_list = ['baidu_weibo']

crawlerprocess = CrawlerProcess(settings)
for spname in spname_list:
    crawler = crawlerprocess.create_crawler(spname)
    spider = crawler.spiders.create(spname)
    crawler.crawl(spider)
crawlerprocess.start()