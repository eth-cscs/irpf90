#!/usr/bin/python

import os

import util
import makefile
import irpf90_t

initialized = False


def init():

  global initialized
  if initialized:
     return

  # Create directories
  for dir in [ irpf90_t.irpdir, irpf90_t.mandir ]:
    try:
      wd = os.getcwd()
      os.chdir(dir)
      os.chdir(wd)
    except OSError:
      os.mkdir(dir)

  # Create makefile
  makefile.create()
  
  # Copy current files in the irpdir
  for filename in os.listdir(os.getcwd()):
    if not filename[0].startswith(".") and not os.path.isdir(filename):
      try:
        file  = open(filename,"r")
      except IOError:
        print "Warning : Unable to read file %s."%(filename)
      else:
        buffer = file.readlines()
        file.close()
        if not util.same_file(irpf90_t.irpdir+filename,buffer):
          file  = open(filename,"r")
          buffer = file.read()
          file.close()
          file = open(irpf90_t.irpdir+filename,"w")
          file.write(buffer)
          file.close()

  initialized = True

