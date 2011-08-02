#!/usr/bin/env python

import argparse
import sys

CITIES = {'shanghai': 021,
        'beijing': 010,
        'suzhou': 0512,
        }

def main():
    parser = argparse.ArgumentParser(
                    description='argparse example')
    parser.add_argument('city',
            choices=CITIES.keys(),
            help='select witch city')
    parser.add_argument('-u','--username',
            help='your username require')
    options = parser.parse_args()
    if options.username not in ['admin']:
        print >> sys.stderr, 'Invalid username'
    print 'Your username is: ', options.username
    print 'Your query city is: ', options.city
    print 'City code is: ', CITIES[options.city]

if __name__ == '__main__':
    main()
