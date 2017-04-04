# -*- coding: utf-8 -*-

import json
from bs4 import BeautifulSoup
import requests
from lxml import etree
from urllib import urlopen
import re
#chrome网页版个人微博主页会通过三次加载AJAX才会全部呈现微博内容
#因此对个人主页的爬取适宜使用手机WAP端
#而对搜索页面的爬取，因单次搜索结果微博只显示前1000条相关结果，需要通过PC网页版的高级分时搜索功能才能全部搜索
#因此对搜索页面的爬取适宜使用PC网页端
#就结果而言两者是差不多的
#但是PC端反爬强度更高
#手机端设置4S的爬取间隔没有问题，但电脑端在爬取1K数据左右后会需要输入验证码

#用来解析定位搜索页面的信息
def transtohtml(s):
	try:
		html = s[(s.index("html")+7):(s.index('"})')-1)]
		real_html=html.replace("\/","/")
		return real_html
	except:
		print "have no html attr"
		return 'error'
#同上定位搜索页面的信息
def transtoHtml(s):
	try:
		html = re.findall(r'(<div class=\\\"search_feed\\\">.*?)\}\)',s)
		# html = re.findall('<div class=\"search_feed\">((.|\\n)*?)"})',s)
		
		# print html[0][0:100]
		if len(html) == 0:
			return 'error'
		return html
	except:
		print "have no such a attr"
		return 'error'
#定位用户微博主页的信息
def TranstoHtml(s):
	try:
		html = re.findall(r'(<div class=\\\"WB_feed WB_feed_v3 WB_feed_v4\\\".*?)\}\)',s)
		if len(html) == 0:
			return 'error'
		return html
	except:
		print "have no such a attr"