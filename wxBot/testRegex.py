#!/usr/bin/env python
# coding: utf-8

import re
s= re.match("[\s\S]*[0-9]{11}[\s\S]*","19812341234")
print s,type(s)
if str(s)=='None':
    print 'none'
else:
    print 'matched'