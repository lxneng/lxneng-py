#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2009-3-12

@author: lxneng
之前说过使用 Python 登陆网站，我们已经可以获取任意一个网址的数据了。但是，在实际应用中，

代理服务器往往是少不了的。在 urllib2 模块中，每一个 opener 可以用多个 handler 来增强功能，

在前一篇，我们使用的是 Cookie 的支持，我们只要在这里再加上 proxy 支持就可以了。
'''
from urllib import urlencode
import cookielib, urllib2
# 准备cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
# 设置代理服务器
proxy_info = {  
        'host' : '127.0.0.1' ,
        'port' : 8118
}
proxy_support = urllib2 . ProxyHandler ( { 'http' : \

        'http://%(host)s:%(port)d' % proxy_info } ) 
# 构造opener
opener = urllib2.build_opener(cookie_support, proxy_support)
urllib2.install_opener(opener)
# 打开网页
page = urllib2.urlopen("http://www.163.com")
print page.read(1000)
page.close()