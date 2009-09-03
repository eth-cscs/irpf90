#!/usr/bin/python

import irpf90_t
irpdir = irpf90_t.irpdir
mandir = irpf90_t.mandir

FILENAME = "Makefile"


def create():
  has_makefile = True
  try:
    file = open(FILENAME,"r")
  except IOError:
    has_makefile = False
  if has_makefile:
    return
  file = open(FILENAME,"w")
  t = """IRPF90 = irpf90  #-a -d
FC     = gfortran
FCFLAGS= -ffree-line-length-none -O2

SRC=
OBJ=
LIB=

include irpf90.make

irpf90.make: $(wildcard *.irp.f)
\t$(IRPF90)
"""
  file.write(t)
  file.close()

