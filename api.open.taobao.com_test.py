#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import string
import time
import md5
import re
import types
import logging
from xml.dom import minidom
import json

#获得当前时间
t = time.localtime()

#参数数组
paramArray = {
	'app_key':'12019613',
    'app_secret':'2a3d1d5eb6e95c28a23b0871bff52bf6',
	'method':'taobao.taobaoke.items.get',
	'format':'json',
	'v':'1.0',
	'timestamp':time.strftime('%Y-%m-%d %X', t),
	#'fields':'iid,title,nick,pic_path,delist_time,price',
    'fields':'iid,title,nick,pic_url,price,click_url,commision,commission_rate,commission_num, commission_volume',
    'keyword':'nike',
    #'nicks':'sandbox_c_1,sandbox_c_12',
    'nick':'lxn2051',
    'session':'26b1b3cf13340ca1878e22b37a66eaad8',
    'page_size':1000,
}

#签名函数
def _sign(param,sercetCode):
	src = sercetCode + ''.join(["%s%s" % (k, v) for k, v in sorted(param.items())])
	return md5.new(src).hexdigest().upper()
	

#生成签名
sign = _sign(paramArray, 'test');
paramArray['sign'] = sign

#组装参数
form_data = urllib.urlencode(paramArray)
#print form_data

#访问服务
urlopen = urllib2.urlopen('http://gw.api.tbsandbox.com/router/rest', form_data)
#urlopen = urllib2.urlopen('http://gw.api.taobao.com/router/rest', form_data)
rsp = urlopen.read();
#rsp = rsp.decode('UTF-8');
print rsp
#data = json.read(str(rsp))
#for item in data['rsp']['items']:
#    print re.sub(r'<[^>]*?>','',item['title']),item.get('nick'),item.get('pic_path')
