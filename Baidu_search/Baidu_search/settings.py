# -*- coding: utf-8 -*-

# Scrapy settings for Baidu_search project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Baidu_search'

EXTENSIIONS_BASE = {
        'scrapy.telnet.TelnetConsole':0,
}

SPIDER_MODULES = ['Baidu_search.spiders']
NEWSPIDER_MODULE = 'Baidu_search.spiders'


ITEM_PIPELINES = {'Baidu_search.pipelines.Mysql_scrapy_pipeline':0}

###################################################################################################

AUTOTHROTTLE_DEBUG=True
AUTOTHROTTLE_START_DELAY=1000
DOWNLOAD_TIMEOUT = 180
#####################################设置下载延迟####################################################
DOWNLOAD_DELAY=4
LOG_FILE=None
LOG_LEVEL='WARNING'

DB_HOST = '127.0.0.1'
DB_NAME = 'root'
DB_PASSWD = 'minus'
DB = 'data'

Sqlite_File = "C:/Users/MINUS/Desktop/ALL/yq_minus/Baidu_search/Baidu_search/test.db"

ENABLE_THREAD_CONTENT = False

LOG_LEVEL='INFO'
LOG_STDOUT=False
LOG_ENABLED=True
LOG_FILE= None