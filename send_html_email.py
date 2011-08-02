#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import urllib2

SMTP_ADDRESS = '74.125.53.109' #gmail smtp
USERNAME = 'lxneng.py@gmail.com'
PASSWORD = 'xxxxxxxx'

def send_html_email(subject, body, to):
    print 'sending......................................'
    handle = smtplib.SMTP(SMTP_ADDRESS,25)
    handle.ehlo()
    handle.starttls()
    handle.ehlo()
    handle.login(USERNAME, PASSWORD)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = USERNAME
    msg['To'] = to
    part2 = MIMEText(body, 'html')
    msg.attach(part2)
    handle.sendmail(USERNAME,[to],msg.as_string())
    handle.quit()
    print 'send complete!'
    return
	
def main():
    parser = argparse.ArgumentParser(
                    description='send html email')
    parser.add_argument('format',
                     choices=['file','url'],
                     help='select format')
    parser.add_argument('--src',
            help='url path or file path')
    parser.add_argument('--title',
            help='subject title')
    parser.add_argument('--to',
            help='send to some body')
    options = parser.parse_args()
    if options.format == 'url':
        body = urllib2.urlopen(options.src).read()
    else:
        body = open(options.src).read()
    send_html_email(options.title, body, options.to)
    
if __name__ == '__main__':
    main()
