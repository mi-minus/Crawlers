# -*- coding: utf-8 -*-
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
from scrapy import log
import settings
import os,time
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

    
class Mysql_scrapy_pipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                                    dbapiName='MySQLdb',
                                    host=settings.DB_HOST,
                                    db=settings.DB,
                                    user=settings.DB_NAME,
                                    passwd=settings.DB_PASSWD,
                                    cursorclass= MySQLdb.cursors.DictCursor,
                                    charset = 'utf8',
                                    use_unicode = False
                                    )
        
    def process_item(self,item,spider):
        self.dbpool.runInteraction(self._conditional_insert,item)
        return item    
        
    def _conditional_insert(self,tx,item): 
    

        # ori_html_path = self.save_html(item)
        # item['repost_post_id'] = ori_html_path
        
        query=u"insert ignore into post (url, topic_id, topic_kws, site_id, site_name, title, content, pt_time, st_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        param=(item['topic_url'], item['topic_id'], item['topic_kw'], item['topic_site_id'], item['topic_site_name'], item['topic_title'], item['topic_content'], item['topic_pt_time'], item['topic_st_time'])
        tx.execute(query,param)
        log.msg('insert one',level=log.WARNING)
        
        # sql = 'insert into '+ item['table_name'] +' (id ,url,board, site_id, data_type , title , content, post_time, scratch_time , poster_name,language_type,repost_post_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE post_time=%s'
        # param = (item['topic_url'],item['topic_url'],item['topic_board'], item['site_id'],item['data_type'],item['topic_title'], item['topic_content'], item['topic_post_time'],item['scratch_time'], item['topic_author'],0,item['repost_post_id'],item['topic_post_time'])
        # tx.execute(sql,param)   
        
    def save_html(self,item):
        os.chdir(r'D:\ori_html\baidu_5')
        sub_dir = 'site_' + str(item['site_id'])
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
        os.chdir(os.path.join(r'D:\ori_html\baidu_5',sub_dir))
        file_name = '%13.0f.html' % (time.time()*1000)
        with open(file_name,'wb') as f:
            f.write(item['thread_content'])
            
        absolute_path = os.path.join(r'D:\ori_html\baidu_5',sub_dir,file_name)
        # print absolute_path
        return absolute_path         
            