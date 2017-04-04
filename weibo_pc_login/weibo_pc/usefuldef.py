# -*- coding: utf-8 -*-
import re
import chardet



# bb=aa.decode("string_escape")  #去掉转义字符

#unicode转成中文
def tranun(s):
	l = len(s)
	ss=''
	i=0
	while i<l:
		try:
			if s[i] =='\\' and s[i+1] =='u':
				ss = ss+unichr(int(s[i+2:i+6],16))
				i += 6
			else:
				ss = ss+s[i]
				i = i+1
		except:
			pass
	return ss
	
#去掉转义字符
def tran(s):
	l = len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\':
			i += 1 
		else:
			ss = ss+s[i]
			i = i+1
	return ss

#去除空格
def deleteSpace(s):
	t = s.strip()
	return t 