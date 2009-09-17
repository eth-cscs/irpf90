#!/usr/bin/python

from irpf90_t import *
from util import *
from variables import variables

FILENAME=irpdir+'irp_touches.irp.F90'

def create():
  out = []
  l = variables.keys()
  l.sort
  for v in l:
    var = variables[v]
    if var.is_touched:
      out += var.toucher

  out = map(lambda x: "%s\n"%(x),out)
  if not same_file(FILENAME,out):
    file = open(FILENAME,'w')
    file.writelines(out)
    file.close()

if __name__ == '__main__':
  create()

