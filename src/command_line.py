#!/usr/bin/python

import getopt, sys
from IRPPython import irp
from version import version

description = "IRPF90 Fortran preprocessor."
options = {}
options['d'] = [ 'debug'        , 'Activate debug', 0 ]
options['v'] = [ 'version'      , 'Print version of irpf90', 0 ]
options['a'] = [ 'assert'       , 'Activate assertions', 0 ]
options['h'] = [ 'help'         , 'Print this help', 0 ]
options['o'] = [ 'openmp'       , 'Activate openMP', 0 ]
options['c'] = [ 'check_cycles' , 'Check cycles in dependencies', 0 ]
options['i'] = [ 'init'         , 'Initialize current directory', 0 ]

class CommandLine(object):

  def __init__(self):
    pass

  def executable_name(self):
    return sys.argv[0]
  executable_name = irp(executable_name,str)

  def usage(self):
    t = """
$EXE - $DESCR

Usage:
  $EXE [OPTION]

Options:
"""
    t = t.replace("$EXE",self.executable_name)
    t = t.replace("$DESCR",description)
    print t
    sorted = options.keys()
    sorted.sort()
    for o in sorted:
     print "  -%s , --%15s : %s"%(o,options[o][0].ljust(15),options[o][1])
     if options[o][2] == 1:
       print "                           Requires an argument"
    print ""
    print "Version : ", version
    print ""

  def opts(self):
    optlist = ["",[]]
    for o in options.keys():
      b = [o]+options[o]
      if b[3] == 1:
        b[0] = b[0]+":"
        b[1] = b[1]+"="
      optlist[0] += b[0]
      optlist[1] += [b[1]]
  
    try:
      opts, args = getopt.getopt(sys.argv[1:], optlist[0], optlist[1])
    except getopt.GetoptError, err:
      # print help information and exit:
      self.usage()
      print str(err) # will print something like "option -a not recognized"
      sys.exit(2)
  
    return opts
  opts = irp(opts,list,tuple,str)
  
  t = """
def do_$LONG(self):
    result = False
    for o,a in self.opts:
      if o in ("-$SHORT", "--$LONG"):
        result = True
        break
    return result
do_$LONG = irp(do_$LONG,bool)
"""
  for short in options.keys():
    long = options[short][0]
    exec t.replace("$LONG",long).replace("$SHORT",short)

  def do_run(self):
   result = not (self.do_version or self.do_init)
   return result
  do_run = irp(do_run,bool)


command_line = CommandLine()
