#!/usr/bin/python

import sys
from irpf90_t import *

######################################################################
def fail(line,message):
  print """
Error:
-----
"""
  print message, '\n'
  if line is not None:
    assert isinstance(line,Line)
    print "file %s ; line %d :\n %s"%(line.filename,line.i,line.text)
  sys.exit(1)


######################################################################
def warn(line,message):
  if line is not None:
    assert isinstance(line,Line)
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

