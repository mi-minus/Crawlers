# -*- coding: utf-8 -*-
# from __future__ import absolute_import, division, print_function#, unicode_literals

import re
import json
import base64
import binascii

import rsa
import requests

# import logging
# logging.basicConfig(level=logging.DEBUG)


WBCLIENT = 'ssologin.js(v1.4.18)'
user_agent = (
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
    'Chrome/20.0.1132.57 Safari/536.11'
)
session = requests.session()
session.headers['User-Agent'] = user_agent


def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)


def wblogin(username, password):
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=%s' % (base64.b64encode(username.encode('utf-8')), WBCLIENT))

    print resp.text
    pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
    pre_login = json.loads(pre_login_str)

    # pre_login = json.loads(pre_login_str)
    # print pre_login['showpin']
    
    code_url ="http://login.sina.com.cn/cgi/pin.php?r=39699013&s=0&p=" + pre_login["pcid"]
    print "---"
    print code_url
    print "---"
    # door = raw_input("input code :")
    
    data = {
        # 'door' : door,
        # 'pcid' : pre_login['pcid'],
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(requests.utils.quote(username).encode('utf-8')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': encrypt_passwd(password, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'rsakv' : pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '72',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data,
    )

    login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',resp.text).group(1)
    print("-----")
    print(login_url)
    resp = session.get(login_url)
    # with open("d:/m.txt","wb") as f:
        # f.write(resp.text)
    login_str = re.match(r'[^{]+({.+?}})', resp.text).group(1)
    return json.loads(login_str)


if __name__ == '__main__':
    print(json.dumps(wblogin('m189111@163.com', 'lianxiang'), ensure_ascii=False))

    # timeline
    homepage = session.get('http://weibo.com/xjtuofficial?is_all=1').text
    with open("d:/mine.html","wb") as f:
    	f.write(homepage)