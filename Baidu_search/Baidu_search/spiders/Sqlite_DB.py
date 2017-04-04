#coding:utf-8

import MySQLdb.cursors
import sqlite3,time
from scrapy import log
from .. import settings
'''
Created on 2015年10月14日

@author: MINUS
'''
class SqliteTime(object):
    def __init__(self,spider_name):
        print settings.Sqlite_File
        self.sx = sqlite3.connect(settings.Sqlite_File) 
        self.cu = self.sx.cursor()
        self.spider_name = spider_name
        self.item_max_time = "2015-5-1 00:00:00"
        self.sqlite_flag = False
        self.item_max_id=''
        self.last_time_sec= self.get_last_time()
        self.scratch_count = 0
        
        
    '''
    从sqlite中读出时间并转化为10位的秒数，如果数据库没有建立或者没数据，将默认值转换并返回
    '''    
    def get_last_time(self):
        try:
            self.cu.execute('CREATE TABLE history (time TEXT,result TEXT,spider_name TEXT primary key)')
            last_time="2015-1-1 00:00:00"
        except:
            try:
                self.cu.execute('SELECT time FROM history where spider_name="'+self.spider_name+'"')
                last_time = self.cu.fetchone()[0]
                log.msg('************* '+last_time,level=log.WARNING)
            except:
                last_time="2015-5-1 00:00:00"
                log.msg('************* '+last_time,level=log.WARNING)
        
        last_time = time.strptime(last_time, '%Y-%m-%d %H:%M:%S')  
        last_time = time.mktime(last_time)     
        return last_time


    '''
    从帖子中拿到时间并比较，参数为item对象数组
    '''
    def get_newest_time(self,itemlists):
        res_items = []
        
        for item in itemlists:
            item_sec = time.mktime(time.strptime(item['topic_pt_time'], '%Y-%m-%d %H:%M:%S'))
            if item_sec >= self.last_time_sec:   #等号用于重复的多爬一次，以对付模糊时间的情况
                self.sqlite_flag = True
                if item_sec > time.time():
                    continue
                
                if item_sec > time.mktime(time.strptime(self.item_max_time, '%Y-%m-%d %H:%M:%S')):
                    self.item_max_time = item['topic_pt_time']
                    self.item_max_id = item['topic_url']
                res_items.append(item)   
                self.scratch_count+=1 
                    
        
        return res_items         
    '''
    参数为一个item对象
    '''
    def get_newest_time_item(self,item):
        item_sec = time.mktime(time.strptime(item['topic_pt_time'], '%Y-%m-%d %H:%M:%S'))
        if item_sec >= self.last_time_sec:     #等号用于重复的多爬一次，以对付模糊时间的情况
            self.sqlite_flag = True
            if item_sec > time.time():
                return False           
            if item_sec > time.mktime(time.strptime(self.item_max_time, '%Y-%m-%d %H:%M:%S')):
                self.item_max_time = item['topic_pt_time']
                self.item_max_id = item['topic_url']

            return True
        return False
    '''
    将最新的数据插入sqlite数据库的操作
    '''    
    def insert_new_time(self): 
        if time.mktime(time.strptime(self.item_max_time, '%Y-%m-%d %H:%M:%S')) < time.time():
            if self.sqlite_flag:
                try:
                    log.msg('delete from history where spider_name='+self.spider_name,level=log.WARNING)
                    self.cu.execute('delete from history where spider_name="'+self.spider_name+'"')
                    self.sx.commit() 
                except sqlite3.OperationalError,e:
                    log.msg('__________',level=log.WARNING)
                    pass
                    
                sql = "insert into history values(?,?,?)"
                params = (self.item_max_time,self.item_max_id,self.spider_name)
                self.cu.execute(sql,params)    
                self.sx.commit() 
        self.close_sqlite()
    
    '''
    关闭数据库
    '''
    def close_sqlite(self):
        print 'sqlite is closed ...'
        self.cu.close()
        self.sx.close()
    
    
    
    
    
    
    
    
    
    