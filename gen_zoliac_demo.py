#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Eric on 2009-09-12.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
def chinese_zodiac(year):
	return u'猴鸡狗猪鼠牛虎兔龙蛇马羊'[year%12]
def zodiac(month, day):
    n = (u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座')  
    d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))  
    return n[len(filter(lambda y:y<=(month,day), d))%12]
def main():
	pass


if __name__ == '__main__':
	main()

