#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by Eric on 2010-02-09.
Copyright (c) 2010 __lxneng@gmail.com__. All rights reserved.
python get_douban_songs_i_like.py -u email -p password
"""
import urllib
import urllib2
import optparse
import re
import socket
import MySQLdb

re_p = re.compile(r'''<tr>.*?<td>(.*?)- <a''', re.S | re.I)
f = None
CONN = MySQLdb.connect(host="localhost", port=3306, user="root", \
                                 passwd="admin", db="test", charset='utf8')
def parse(html):
	#print html
	db_cursor = CONN.cursor()
	m = re_p.findall(html)
	if m:
		for song_name in m:
			song_name = song_name.strip()
			if 'align' not in song_name:
				print song_name
				try:
					db_cursor.execute('''insert into douban_songs(name) values (%s)''', song_name)
				except:
					continue
				f.write(song_name.strip()+'\n')
		return True
		CONN.commit()
	else:
		return False
def fetch(email, password):
	c = urllib2.HTTPCookieProcessor()
	builder = urllib2.build_opener(c)
	request = urllib2.Request('http://www.douban.com/login',\
	 data = urllib.urlencode({'form_email':email,'form_password':password}))
	rsp = builder.open(request)
	i = 0
	while 1:
		url = 'http://douban.fm/mine?start=%s&type=like'%i
		print url
		request = urllib2.Request(url)
		rsp = builder.open(request)
		if parse(rsp.read()):
			i+=20
		else:
			break
	
def main():
	global f
	f = open('songs.txt', 'wb')
	usage = 'usage: %prog -u email -p password'
	parser = optparse.OptionParser(usage)
	parser.add_option('-u', '--email', dest='email', help='-u email', type='string')
	parser.add_option('-p', '--password', dest='password', help='-p password', type='string')
	(options, args) = parser.parse_args()
	if options.email == None:
		parser.error('must has -u option!')
	if options.password == None:
		parser.error('must has -p option!')
	fetch(options.email, options.password)
	f.close()
if __name__ == '__main__':
	main()