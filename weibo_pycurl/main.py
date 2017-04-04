#coding=utf-8
import pycurl
import StringIO
import re,chardet

import os,time
import MySQLdb as mdb
import urllib

os.chdir(r'D:\crawler\weibo_pycurl')
print os.getcwd()
import sys;
sys.path.append("d:/crawler/weibo_pycurl")

import setting,db_setting

def tranun(s):
	l=len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\' and s[i+1]=='u':
			ss=ss+unichr(int(s[i+2:i+6],16))
			i=i+6
		else:
			ss=ss+s[i]
			i=i+1
	return ss
def tran(s):
	l=len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\':
			i=i+1
		else:
			ss=ss+s[i]
			i=i+1
	return ss

def main(con):
	
	b=tranun(con)
	c=tran(b)
	pattern=re.compile(r'rnt{0,25}|t{3,25}',re.S)
	pattern1=re.compile(r'>n*\s*t*\s*t*',re.S)
	c=re.sub(pattern,'',c)
	c=c.replace('n<','<')
	d=re.sub(pattern1,'>',c)
	d=d.encode('utf-8')

    
	file_path=setting.CURRENT_PATH+'/res.txt'
	f=open(file_path,'wb')
	f.write(d)
	f.close()
	
def getpage(url):
    c=pycurl.Curl()
    print url
    c.setopt(pycurl.URL,url)
    
    b=StringIO.StringIO()
    print '1'
    c.setopt(pycurl.WRITEFUNCTION,b.write)
    print '2'
    c.perform()
    print '-----'
    # f=open('%s/posts.txt' % setting.CURRENT_PATH,'wb')
    # f.write(b.getvalue())
    # f.close()
    return b.getvalue()
    
def cutpage(html):
    patt=re.compile('{"pid":"pl_weibo_direct".*?<script>STK',re.S)
    con=re.findall(patt,html)[0]
    f=open('d:/mii.txt','wb')
    f.write(con)
    f.close()
    return con
    
def write_local(html,kwd,path):
    file_name = '13_'+kwd+'_'+str(int(time.time()))+'.txt'
    with open(path+'/'+file_name,'wb') as f:
        # print path+'/'+file_name
        # print '&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        f.write(html)
    
    
if __name__=='__main__':

    # topic_dict = {'1':[u'考试', u'分数'], '2':['北京','西安']}
    # topic_dict = {'1':[u'萨德'], '2':[u'两会'], '3':[u'西安地铁']}
    topic_dict = {'1':[u'萨德'], '2':[u'两会'], '3':[u'西安地铁'], '4':[u'雄安']}
    for id, kws_list in topic_dict.iteritems():
        for kw in kws_list:
            topid = int(id)
            kwd = kw
            
        # for out_ll in topic_dict:
            # kw_num = len(out_ll.items()[0][1])
            # topid = out_ll.items()[0][0]
            # kwd = out_ll.items()[0][1][cnt%kw_num]
            # print kwd
            
            #####################################################################################3

            #####################################################################################
            #####################################################################################
            
            kwd=kwd.encode('utf-8')
            kwd=urllib.quote(kwd)
            print kwd
            while 1:
                try:
                    html=getpage('http://s.weibo.com/weibo/'+kwd+'&xsort=time&Refer=weibo_wb')
                except:
                    print 'try again...'
                    continue
                break
                
            # write_local(html,kwd,new_path)
            #html=getpage('http://s.weibo.com/wb/%25E6%25A6%2586%25E6%259E%2597&xsort=time&page=3')
            content=cutpage(html)
            main(content)

            os.system('python %s/parse_post.py %d %s' % (setting.CURRENT_PATH ,topid,kw))
            time.sleep(50)                
            
            
    cur.close()
    conn.close()