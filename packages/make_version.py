#!/usr/bin/python

import sys, os
wd = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,(wd+"/../src/"))
from version import *
print "VERSION=%s"%(version)
