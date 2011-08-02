#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 lxneng@gmail.com.
# 
__author__ = 'lxneng@gmail.com (Eric Lo)'

import os
import urllib2
import StringIO
import gzip
import urllib
import random
import socket
socket.setdefaulttimeout(100)


PROXY_LIST = ['http://221.130.13.204:80', 
              'http://202.108.22.159:80',
              'http://127.0.0.1:80',
              'http://58.221.41.91:80',
              'http://218.17.5.151:80',
              'http://199.239.136.200:80',
              ]
USER_AGENT_LIST = [
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
                   "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1; .NET CLR 1.1.4322)",
                   "Opera/9.20 (Windows NT 6.0; U; en)",
                   "Opera/9.00 (Windows NT 5.1; U; en)",
                   'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.50",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0",
                   "Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1",
                    ]
def fetchHtml( url = None ):
    if (url == None):
        return ""
    html = ""
    txdata = None
    txheaders = {   
        'User-Agent': random.choice(USER_AGENT_LIST),
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'gzip, deflate, compress;q=0.9',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http':random.choice(PROXY_LIST)}))
    urllib2.install_opener(opener)
    req = urllib2.Request(url, txdata, txheaders)
    try:
        handle = urllib2.urlopen(req)
        try:
            if handle.info()['Content-Encoding'] == "gzip":
                html = gzip.GzipFile('','r',0,StringIO.StringIO(handle.read())).read()
            else:
                html = handle.read()
            #html = html.decode('gb2312', 'replace').encode('utf8', 'replace')
        except:
            response = urllib.urlopen(url)
            html = response.read()
    except IOError, e:
        pass
    return html
