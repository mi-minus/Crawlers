# encoding=utf-8
import json
import base64
import requests
import re, random, string, os
import binascii
import rsa

"""
输入你的微博账号和密码，可去淘宝买，一元七个。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
    # {'no': 'a759451@drdrb.net', 'psw': '5007734'},
    {'no': '18392886307', 'psw': 'gongli401'},
    # {'no': '13572021695', 'psw': 'lcxsw616'},
]


def getCookies_without_pic(weibo):
    """ 获取Cookies """
    cookies = []
    
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            print "Get Cookie Success!( Account:%s )" % account
            cookie = session.cookies.get_dict()
            # print  cookie
            cookies.append(cookie)
        else:
            print "Failed!( Reason:%s )" % info['reason']
    return cookies
########################################################################################################

def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)


def getCookies_with_pic(weibo):

    WBCLIENT = 'ssologin.js(v1.4.18)'
    user_agent = (
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
        'Chrome/20.0.1132.57 Safari/536.11'
    )
    cookies = []
    for elem in weibo:
        username = elem['no']
        password = elem['psw']
        session = requests.Session()
        session.headers['User-Agent'] = user_agent
        
        resp = session.get('http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=%s' % (base64.b64encode(username.encode('utf-8')), WBCLIENT))

        pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
        pre_login = json.loads(pre_login_str)

        # print resp.text
        
        '''
        验证码随机生成
        '''
        salt = ''.join(random.sample(string.digits, 8))
        code_url ="http://login.sina.com.cn/cgi/pin.php?r="+salt+"s=0&p=" + pre_login["pcid"]
        print "---"
        print code_url
        print "---"
        pic_content = session.get(code_url,stream=True).content
        '''
        将验证码保存下来
        '''
        
        with open('d:/pic.png','wb') as f:
            f.write(pic_content)
        
        os.system('d:/pic.png')
        
        door = raw_input("input code :")
        
        data = {
            'door' : door,
            'pcid' : pre_login['pcid'],
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
            'prelt': '57',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
                   'naSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        resp = session.post(
            'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
            data=data,
        )
        try:
            login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',resp.text).group(1)
            print login_url
            resp = session.get(login_url)

            login_str = re.match(r'[^{]+({.+?}})', resp.text).group(1)
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
            print "Get Cookie Success!( Account:%s )"
        except:
            print "Failed!( Reason:%s )"
    return cookies

cookies = getCookies_with_pic(myWeiBo)
print "Get Cookies Finish!( Num:%d)" % len(cookies)
