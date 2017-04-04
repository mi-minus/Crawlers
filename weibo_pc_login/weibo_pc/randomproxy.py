#coding: utf-8
'''
Created on 2015年12月21日

@author: MINUS
'''
import re
import random
import base64
from scrapy import log
class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)
        self.proxies = {}
        for line in fin.readlines():
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)
            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else: 
                user_pass = ''
            self.proxies[parts.group(1) + parts.group(3)] = user_pass
        fin.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return
        proxy_address = random.choice(self.proxies.keys())
        print '+++++++++++++++++++++' + proxy_address
        proxy_user_pass = self.proxies[proxy_address]
        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            print '------------'
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth
        
    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        log.msg('Removing failed proxy <%s>, %d proxies left' % (
                                                                 proxy, len(self.proxies)))
        try:
            del self.proxies[proxy]
        except ValueError:
            pass
        
        
        
        