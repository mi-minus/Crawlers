# -*- coding: utf-8 -*-
import requests
import json
import chardet
from bs4 import BeautifulSoup
import sys,time
from weibo_sp import get_sp_rsa

s = requests.session()

message_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=YXNkZg%3D%3D&rsakt=mod&checkpin=1&client=ssologin.js%28v1.4.18%29"

r1 = s.get(message_url)

source_page = r1.text[35:-1]
json_items = json.loads(source_page)
retcode = json_items['retcode']
servertime = json_items['servertime']
pcid = json_items['pcid']
nonce = json_items['nonce']
pubkey = json_items['pubkey']
rsakv = json_items['rsakv']
is_openlock = json_items['is_openlock']
showpin = json_items['showpin']
exectime = json_items['exectime']

request_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

sp = get_sp_rsa("lianxiang",servertime,nonce)

data = {
    'door' : door,
    'encoding' : 'UTF-8',
    'entry' : 'weibo',
    'from' : '',
    'gateway' : '1',
    'nonce' : nonce,
    'pagerefer' : '',
    'pcid' : pcid,
    'prelt' : '72',
    'pwencode' : 'rsa2',
    'returntype' : 'META',
    'rsakv' : rsakv,
    'savestate' : '7',
    'servertime' : servertime,
    'service' : 'miniblog',
    'sp' : sp,
    'sr' : '1696*954',
    'su' : 'bTE4OTExMSU0MDE2My5jb20=',
    'url' : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'useticket' : '1',
    'vsnf' : '1',
}





