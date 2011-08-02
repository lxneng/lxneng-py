#!/usr/bin/env python
# -*- coding: utf-8 -*-
import optparse
     
def main():
    usage = 'usage: %prog -p name'
    p = optparse.OptionParser(usage)
    p.add_option('--person', '-p', default="world")
    options, arguments = p.parse_args()
    print 'Hello %s' % options.person
      
if __name__ == '__main__':
    main()

