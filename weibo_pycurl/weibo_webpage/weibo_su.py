#coding:utf-8
import urllib,base64

def get_su(user_name):
    username_ = urllib.quote(user_name)     # html×Ö·û×ªÒå
    username = base64.encodestring(username_)[:-1]
    return username
    
print get_su("18702978864")