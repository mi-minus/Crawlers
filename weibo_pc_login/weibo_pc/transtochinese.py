#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
from usefuldef import tranun
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect("localhost","root","gongli","sina_spider_db",charset="utf8mb4")

cursor = db.cursor()

sql0 = "SET NAMES utf8mb4;"
cursor.execute(sql0)

sql = "SELECT * FROM test_table_3 "


cursor.execute(sql)

results = cursor.fetchall()

for result in results:
	data_id = result[0]
	u_name = result[1]
	u_content = result[3]
	print u_name,type(u_name)
	print u_content,type(u_content)
	if u_name != None:

		u_name1 = u_name.strip()
		real_u_name = tranun(u_name1)

		u_content1 = u_content.strip()
		real_u_content = tranun(u_content1)
		print u_name1
		print u_content1
		print real_u_content
		print real_u_name
		try:
			sql1 = "UPDATE test_table_3 SET u_name='%s', u_content='%s' WHERE id=%s" % (real_u_name, real_u_content, data_id)
			cursor.execute(sql1)
			db.commit()
		except:
			db.rollback()



db.close()



