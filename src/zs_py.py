# -*- coding: utf-8 -*-
import os
import re
import random



#---------------------------------------------------------------------------------------#
#                             Regular expression
#---------------------------------------------------------------------------------------#


'''
sys.path.insert(0, '../')
import zs_py as zp

Usage 1:

if zp.regex(re.match, r'(a)bc', 'abcd', 0, zp.r):
    print(zp.r.m.group(1))


Usage 2:

r = zp.RegexResult()
if zp.regex(re.match, r'(a)bc', 'abcd', re.DOTALL|re.X, r):
    print(r.m.group(1))
    

'''
#---------------
class RegexResult:
    def __init__(self):
        self.m = None

r = RegexResult()

def regex(re_func, pattern, string, flags, r):
    r.m = None
    r.m = re_func(pattern, string, flags)
    return r.m

#---------------------------------------------------------------------------------------#
#                             Nested Dictionary
#---------------------------------------------------------------------------------------#
class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]