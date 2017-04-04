#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import sys
import traceback
import json
reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect("localhost","root","gongli","sina_spider_db",charset="utf8mb4")

cursor = db.cursor()

sql0 = "SET NAMES utf8mb4;"
cursor.execute(sql0)

sql = "SELECT * FROM test_table_3  WHERE timeunix >= 1481299200 AND timeunix <= 1484064000 ORDER BY timeunix ASC"
cursor.execute(sql)
results = cursor.fetchall()

with open('data_12_10_to_1_11.txt','wb') as file_str:
    for result in results:
        try:
            u_name = result[1]
            u_id = result[2]
            u_content = result[3]
            u_gmttime = result[4]
            u_timeunix = result[5]

            data = []
            hashtags = []
            users = []
            urls = []
            media_urls = []
            nfollowers = 100
            nfriends = 100
            users.append(u_name)

            data.append(u_timeunix)
            data.append(u_gmttime)
            data.append(u_id)
            data.append(u_content)
            data.append(hashtags)
            data.append(users)
            data.append(urls)
            data.append(media_urls)
            data.append(nfollowers)
            data.append(nfriends)

            data_pack = json.dumps(data)

            file_str.write(data_pack)
            file_str.write('\n')
        except:
            print traceback.print_exc()