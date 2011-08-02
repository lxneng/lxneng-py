import sys
import subprocess
from os import environ

if 'VIRTUAL_ENV' in environ:
    path = subprocess.Popen(['python', '-c','import sys;print(repr(sys.path))'],
                            stdout=subprocess.PIPE).communicate()[0]
    sys.path = eval(path)
    del path

del sys, subprocess, environ
