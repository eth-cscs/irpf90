#!/usr/bin/python

import sys
from irpf90_t import *

######################################################################
def fail(line,message):
  assert isinstance(line,Line)
  print """
Error:
-----
"""
  if line.i > 0:
    print "file %s, line %d:\n%s"%(line.filename,line.i,line.text)
  print message, '\n'
  sys.exit(1)


######################################################################
def warn(line,message):
  assert isinstance(line,Line)
  print """
Warning:
-------
"""
  if line.i > 0:
    print "file %s, line %d:\n%s"%(line.filename,line.i,line.text)
  print message, '\n'


######################################################################
if __name__ == '__main__':
  line = Empty_line(3,"empty", "testfile")
  fail(line, "Message")

