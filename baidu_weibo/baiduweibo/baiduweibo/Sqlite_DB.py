#coding:utf-8


import sqlite3,time
import logging
from baiduweibo.settings import LAST_TIME
import calendar,os
import settings


class SqliteTime(object):
    def __init__(self,spider_name):
        self.sx = sqlite3.connect('/home/yuqing/Scrapy_crawlers/GaoKao/tianya_spider/tianya/test.db')  #或r'\test.db'
        self.cu = self.sx.cursor()
        self.spider_name = spider_name
        self.sqlite_flag = False
        
        self.last_time = self.get_last_time()
        self.result = ''
#        self.site_max_time = dict(self.site_dict)   #不能写成self.site_max_time = self.site_dict，改变self.site_max_time时也会改变site_dict
        self.item_max_time = self.last_time
        self.item_max_id=''


    '''
    从sqlite中读出时间并转化为10位的秒数，如果数据库没有建立或者没数据，将默认值转换并返回
    '''    
    def get_last_time(self):
        try:
            self.cu.execute('CREATE TABLE history (time TEXT,result TEXT,spider_name TEXT primary key)')
            last_time = LAST_TIME
        except:
            try:
                self.cu.execute('SELECT time,result FROM history where spider_name="'+self.spider_name+'"')
                re = list(self.cu.fetchone())#fetchone()返回的是元祖tuple
                last_time = re[0]
                self.result = re[1]
            except:
                print "%%%%%%%%%%"
                last_time = LAST_TIME
        last_time = time.strptime(last_time, '%Y-%m-%d %H:%M:%S')       
        return last_time

       
    '''
    参数为一个item对象
    '''
    def get_newest_time(self,post_time,url):
        item_sec = time.strptime(post_time, '%Y-%m-%d %H:%M:%S')
        if calendar.timegm(item_sec) >= calendar.timegm(self.last_time) and url != self.result:     #等号用于重复的多爬一次，以对付模糊时间的情况
            self.sqlite_flag = True
            if calendar.timegm(item_sec) >= calendar.timegm(self.item_max_time):
                self.item_max_time = item_sec
                self.item_max_id = url
            return True
        return False
    
    '''
    将最新的数据插入sqlite数据库的操作
    '''    
    def insert_new_time(self): 
        if self.sqlite_flag: 
            self.item_max_time = time.strftime('%Y-%m-%d %H:%M:%S',self.item_max_time)
            sql = 'replace into history(time,result,spider_name) values (?,?,?)'
            print '---------self.item_max_id-----------',self.item_max_id
            print '--item_max_time =', self.item_max_time
            print '--spider_name =', self.spider_name
            params = (self.item_max_time,self.item_max_id,self.spider_name)
            self.cu.execute(sql,params)    
            self.sx.commit() 
        self.close_sqlite()
       

    
    '''
    关闭数据库
    '''
    def close_sqlite(self):
#         print 'sqlite is closed ...'
        self.cu.close()
        self.sx.close()
    
    
    
    
    
    
    
    
    
    
