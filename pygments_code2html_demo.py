#!/usr/bin/env python
# encoding: utf-8
"""
pygments_code2html_demo.py

Created by Eric on 2009-09-14.
Copyright (c) 2009 __lxneng@gmail.com__. All rights reserved.
"""

import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def code2html(code, lang):
    lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True)
    formatter = HtmlFormatter(
            linenos=False,
            encoding='utf-8',
            noclasses="True")
    result = highlight(code, lexer, formatter)
    return result

def demo():
    f = open(__file__)
    code = f.read()
    f.close()
    html = """
	<html>
	    <head>
	        <title>Pygments_example</title>
	    </head>
	    <body>
	    %s
		</body>
	</html>
	"""%code2html(code, 'python')
    print html
    ff = open('test.html','w')
    ff.write(html)
    ff.close()
if __name__ == '__main__':
    demo()

