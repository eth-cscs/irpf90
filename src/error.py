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
  print message, '\n'
  if line is not None:
    print "file %s ; line %d :\n %s"%(line.filename,line.i,line.text)
  sys.exit(1)


######################################################################
def warn(line,message):
  assert isinstance(line,Line)
  if line is not None:
    print """
Warning:
-------
"""
    print message, '\n'
    print "file %s, line %d:\n %s"%(line.filename,line.i,line.text)
  else:
    print "Warning: %s"%(message)


######################################################################
if __name__ == '__main__':
  line = Empty_line(3,"empty", "testfile")
  fail(line, "Message")

