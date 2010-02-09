#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from pydelicious import DeliciousAPI
#from getpass import getpass

#user = raw_input("Username:")
#a = DeliciousAPI(user,getpass("Password:"))
import pydelicious

for rec in pydelicious.get_popular(tag='python'):
	print rec.get('href'),rec.get('tags')
	
for rec in pydelicious.get_userposts('lxneng'):
	print rec.get('href'),rec.get('tags')
	
	
