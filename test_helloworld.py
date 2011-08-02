#!/usr/bin/env python

# -*- coding: utf-8 -*-

#from re import sub,compile
#from MySQLdb import connect
#from cx_Oracle import connect

import re
import MySQLdb
import cx_Oracle

def hello():
    print 'Hello World!'

def connect_to_mysql(hostname,mysqlport,username,password,database,conncharset):
    try:
        conn = MySQLdb.connect(host=host, port=mysqlport, user=username,\
                            passwd=password, db=database, charset=conncharset)
    except BaseException ,e:
        print e
    return True 
def connect_to_whitout_dsn(username,password,hostname,port,dbname):
    
    dsn=cx_Oracle.makedsn(hostname, port, dbname)
    connection=cx_Oracle.connect(username, password, dsn)
    
    return True 
def connect_with_dsn(username,password,dsn):
    
    connection=cx_Oracle.connect(username, password, dsn)
    
    return True 
