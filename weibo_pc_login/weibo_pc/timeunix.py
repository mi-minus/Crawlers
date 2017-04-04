#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
from usefuldef import tranun
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect("localhost","root","gongli","sina_spider_db",charset="utf8mb4")

cursor = db.cursor()

sql0 = "SET NAMES utf8mb4;"
cursor.execute(sql0)

sql = "SELECT * FROM test_table_3"

cursor.execute(sql)

results = cursor.fetchall()
for result in results:
    data_id = result[0]
    
    try:
        result_time = result[4] + ":00"
        timeArray = time.strptime(result_time,"%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        time_unix = int(timestamp)
        try:
            sql2 = "UPDATE test_table_3 SET timeunix='%s' WHERE id=%s" % (time_unix, data_id)
            cursor.execute(sql2)
            db.commit()
        except:
            db.rollback()
    except:
        try:
            sql3 = "UPDATE test_table_3 SET timeunix=1481723160 WHERE id=%s" % (data_id)
            cursor.execute(sql3)
            db.commit()
        except:
            db.rollback()

db.close()