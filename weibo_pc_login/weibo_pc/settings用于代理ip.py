# -*- coding: utf-8 -*-

# Scrapy settings for qian project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'qian'

SPIDER_MODULES = ['qian.spiders']
NEWSPIDER_MODULE = 'qian.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qian (+http://www.yourdomain.com)'#
ITEM_PIPELINES = {'qian.pipelines.JuanKuanPipeline':1,}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    # Fix path to this module
#     'qian.randomproxy.RandomProxy': 100,
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}
PROXY_LIST = 'D:/Work_space/Java/Spider_demo/qian/list.txt'

DOWNLOAD_DELAY=2.8
COOKIES_ENABLED = False
REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True
ROBOTSTXT_OBEY = True

Sqlite_File = 'D:/Work_space/Java/Spider_demo/qian/test.db'
