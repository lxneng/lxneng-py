#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2010 __lxneng@gmail.com__. All rights reserved.
"""
import time,datetime
import threading

def worker(a_tid, a_account):
	global g_mutex
	print 'Start', a_tid, datetime.datetime.now()
	for i in range(1000000):
		g_mutex.acquire()
		a_account.deposite(1)
		g_mutex.release()
	print "End", a_tid, datetime.datetime.now()

class Account(object):
	def __init__(self,a_base):
		self.m_amount=a_base
	def deposite(self, a_amount):
		self.m_amount+=a_amount
	def withdraw(self, a_amount):
		self.m_amount-=a_amount
def main():
	global g_mutex
	count = 0
	dstart = datetime.datetime.now()
	print 'Main Thread Start At:',dstart 
	
	#init thread_pool
	thread_pool = []
	#init mutex
	g_mutex = threading.Lock()
	# init thread items
	acc = Account(100)
	for i in range(10):
		th = threading.Thread(target=worker, args=(i, acc))
		thread_pool.append(th)
	# start threads one by one
	for i in range(10):
		thread_pool[i].start()
	
	#collect all threads
	for i in range(10):
		threading.Thread.join(thread_pool[i])
	dend = datetime.datetime.now()
	print 'count=', acc.m_amount
	print 'Main Thread End at: ', dend, 'time span', dend-dstart 

if __name__ == "__main__":
	main()		
