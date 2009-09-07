#!/usr/bin/python

from variable  import Variable
from variables import variables
from irpf90_t  import *

def do_size(l):
  if l == []: return ""
  else:       return "(%s)"%(",".join(l))

def do_print_short(file,var):
  assert isinstance(var,Variable)
  print >>file, "%s : %s :: %s %s"%( \
   var.line.filename,
   var.type,
   var.name,
   do_size(var.dim) )

######################################################################
def process_doc(file,line):
  assert isinstance(line,str)
  line = line.strip()
  if line == "":
    line = ".br"
  print >>file, line

######################################################################
def process_deps(file,l):
  assert isinstance(l,list)
  for v in l:
    print >>file, "%s\n.br"%(v,)

######################################################################
def process_types(file,var):
  assert isinstance(var,Variable)
  vars = [var.name] + var.others
  for var in vars:
    name = var
    var = variables[var]
    type = var.type
    dim = do_size(var.dim)
    print >>file, "%s\t:: %s\t%s"%(type,name,dim)

######################################################################
def do_print(var):
  assert isinstance(var,Variable)
  filename = var.line.filename
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
    print >>file, ".SH Needs"
    process_deps(file,var.needs)
  if var.needed_by != []:
    print >>file, ".SH Needed by"
    process_deps(file,var.needed_by)
  file.close()

######################################################################
def run():
  import parsed_text
  file = open("irpf90_entities","w")
  for v in variables.keys():
    do_print_short(file,variables[v])
  file.close()
  for v in variables.keys():
    do_print(variables[v])

######################################################################
if __name__ == '__main__':
  run()
