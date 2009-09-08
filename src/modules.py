#!/usr/bin/python

from irpf90_t import *
from parsed_text import parsed_text
from module import Fmodule
from util import *

######################################################################
def create_modules():
  result = {}
  for filename,text in parsed_text:
    result[filename] = Fmodule(text,filename)  
  return result

modules = create_modules()

######################################################################
def write_module(m):
  filename = irpdir+m.name[0:-4]+".irp.F90"
  text = m.head + m.generated_text + m.residual_text
  text = map(lambda x: "%s\n"%(x),text)
  if not same_file(filename,text):
    print filename
    file = open(filename,"w")
    file.writelines(text)
    file.close()

######################################################################
if __name__ == '__main__':
  write_module(modules['electrons.irp.f'])
  

