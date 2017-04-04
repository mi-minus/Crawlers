#coding=utf-8

import os,time
import setting
i=1
while 1:
    os.system('python %s/main.py' %setting.CURRENT_PATH)
    print 'start waiting...'
    print 'start '+ str(i) +' times'
    i+=1
    time.sleep(600)