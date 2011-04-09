#!/usr/bin/python
#   IRPF90 is a Fortran90 preprocessor written in Python for programming using
#   the Implicit Reference to Parameters (IRP) method.
#   Copyright (C) 2009 Anthony SCEMAMA 
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   Anthony Scemama
#   LCPQ - IRSAMC - CNRS
#   Universite Paul Sabatier
#   118, route de Narbonne      
#   31062 Toulouse Cedex 4      
#   scemama@irsamc.ups-tlse.fr


from variable  import Variable
from variables import variables
from irpf90_t  import *
from util import *


def do_print_short(file,var):
  assert type(var) == Variable
  print >>file, "%s : %s :: %s %s"%( \
   var.line.filename[0].ljust(25),
   var.type.ljust(25),
   var.name.ljust(25),
   build_dim(var.dim) )

######################################################################
def process_doc(file,line):
  assert type(line) == str
  line = line.strip()
  if line == "":
    line = ".br"
  print >>file, line

######################################################################
def process_deps(file,l):
  assert type(l) == list
  for v in l:
    print >>file, "%s\n.br"%(v,)

######################################################################
def process_types(file,var):
  assert type(var) == Variable
  vars = [var.name] + var.others
  for var in vars:
    name = var
    var = variables[var]
    Type = var.type
    dim = build_dim(var.dim)
    print >>file, "%s\t:: %s\t%s"%(Type,name,dim)

######################################################################
def do_print(var):
  assert type(var) == Variable
  filename = var.line.filename[0]
  name = var.name
  file = open("%s%s.l"%(mandir,var.name), "w")
  print >>file, '.TH "IRPF90 entities" l %s "IRPF90 entities" %s'%(name,name)
  if var.same_as != var.name:
    var = variables[var.same_as]
  print >>file, ".SH Declaration"
  print >>file, ".nf"
  process_types(file,var)
  print >>file, ".ni"
  if var.doc != []:
   print >>file, ".SH Description"
   for l in var.doc:
     process_doc(file,l)
  print >>file, ".SH File\n.P"
  print >>file, filename
  if var.needs != []:
    var.needs.sort()
    print >>file, ".SH Needs"
    process_deps(file,var.needs)
  if var.needed_by != []:
    var.needed_by.sort()
    print >>file, ".SH Needed by"
    process_deps(file,var.needed_by)
  file.close()

######################################################################
def run():
  import parsed_text
  import os,sys
  if os.fork() == 0:
    for v in variables.values():
      do_print(v)
    sys.exit(0)

  if os.fork() == 0:
    l = variables.keys()
    file = open("irpf90_entities","w")
    l.sort()
    for v in l:
      do_print_short(file,variables[v])
    file.close()
    sys.exit(0)

######################################################################
if __name__ == '__main__':
  run()
