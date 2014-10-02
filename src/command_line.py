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


import getopt, sys
from version import version
import re

description = "IRPF90 Fortran preprocessor."
options = {}
options['a'] = [ 'assert'       , 'Activates ASSERT statements. If absent, remove ASSERT statements.', 0 ]
options['c'] = [ 'codelet'      , 'entity:NMAX or entity:precondition:NMAX  : Generate a codelet to profile a provider running NMAX times', 1 ]
options['C'] = [ 'coarray'      , 'All providers are coarrays', 0 ]
options['d'] = [ 'debug'        , 'Activates debug. The name of the current subroutine/function/provider will be printed on the standard output when entering or exiting a routine, as well as the CPU time passed inside the routine.', 0 ]
options['D'] = [ 'define'       , 'Defines a variable identified by the IRP_IF statements.', 1 ]
options['g'] = [ 'profile'      , 'Activates profiling of the code.', 0 ]
options['h'] = [ 'help'         , 'Print this help', 0 ]
options['I'] = [ 'include'      , 'Include directory', 1 ]
options['i'] = [ 'init'         , 'Initialize current directory. Creates a default Makefile and the temporary working directories.', 0 ]
options['l'] = [ 'align'        , 'Align arrays using compiler directives and sets the $IRP_ALIGN variable. For example, --align=32 aligns all arrays on a 32 byte boundary.', 1 ]
options['m'] = [ 'memory'       , 'Print memory allocations/deallocations.', 0 ]
options['n'] = [ 'inline'       , 'all|providers|builders : Force inlining of providers or builders', 1 ]
options['o'] = [ 'checkopt'     , 'Shows where optimization may be required', 0 ]
options['p'] = [ 'preprocess'   , 'Prints a preprocessed file to standard output. Useful for  debugging files containing shell scripts.', 1 ]
options['r'] = [ 'no_directives', 'Ignore all compiler directives !DEC$ and !DIR$', 0 ]
options['s'] = [ 'substitute'   , 'Substitute values in do loops for generating specific optimized code.', 1 ]
options['t'] = [ 'touch'        , 'Display which entities are touched when touching the variable given as an argument.', 1 ]
options['u'] = [ 'unused'       , 'Print unused providers', 0 ]
options['v'] = [ 'version'      , 'Prints version of irpf90', 0 ]
#options['z'] = [ 'openmp'       , 'Automatic openMP tasks (may not work)', 0 ]

class CommandLine(object):

  do_openmp = False
  def __init__(self):
    global options
    self._opts = None
    self.argv = list(sys.argv)
    self.executable_name = self.argv[0]

  def defined(self):
    if '_defined' not in self.__dict__:
      self._defined = []
      for o,a in self.opts:
        if o in [ "-D", '--'+options['D'][0] ]:
          self._defined.append(a)
    return self._defined
  defined = property(fget=defined)

  def include_dir(self):
    if '_include_dir' not in self.__dict__:
      self._include_dir = []
      for o,a in self.opts:
        if o in [ "-I", '--'+options['I'][0] ]:
          if len(a) < 1: 
            print "Error: -I option needs a directory"
          if a[-1] != '/':
            a = a+'/'
          self._include_dir.append(a)
    return self._include_dir
  include_dir = property(fget=include_dir)

  def inline(self):
    if '_inline' not in self.__dict__:
      self._inline = ""
      for o,a in self.opts:
        if o in [ "-n", '--'+options['n'][0] ]:
          self._inline = a
          break
    return self._inline
  inline = property(fget=inline)

  def substituted(self):
    if '_substituted' not in self.__dict__:
      self._substituted = {}
      for o,a in self.opts:
        if o in [ "-s", '--'+options['s'][0] ]:
          k, v = a.split(':')
          v_re = re.compile(r"(\W)(%s)(\W.*$|$)"%k.strip())
          self._substituted[k] = [v, v_re]
    return self._substituted
  substituted = property(fget=substituted)

  def codelet(self):
    if '_codelet' not in self.__dict__:
      self._codelet = []
      for o,a in self.opts:
        if o in [ "-c", '--'+options['c'][0] ]:
          buffer = a.split(':')
          filename = 'codelet_'+buffer[0]+'.irp.f'
          if len(buffer) == 2:
            self._codelet = [buffer[0], int(buffer[1]), None, filename]
          elif len(buffer) == 3:
            self._codelet = [buffer[0], int(buffer[2]), buffer[1], filename]
          else:
            print """
Error in codelet definition. Use:
--codelet=provider:NMAX
or
--codelet=provider:precondition:NMAX
"""
            sys.exit(1)
    return self._codelet
  codelet = property(fget=codelet)

  def preprocessed(self):
    if '_preprocessed' not in self.__dict__:
      self._preprocessed = []
      for o,a in self.opts:
        if o in [ "-p", '--'+options['p'][0] ]:
          self._preprocessed.append(a)
    return self._preprocessed
  preprocessed = property(fget=preprocessed)

  def touched(self):
    if '_touched' not in self.__dict__:
      self._touched = []
      for o,a in self.opts:
        if o in [ "-t", '--'+options['t'][0] ]:
          self._touched.append(a.lower())
    return self._touched
  touched = property(fget=touched)

  def align(self):
    if '_align' not in self.__dict__:
      self._align = '1'
      for o,a in self.opts:
        if o in [ "-l", '--'+options['l'][0] ]:
          self._align = a
    return self._align
  align = property(fget=align)

  def coarray(self):
    if '_coarray' not in self.__dict__:
      self._coarray = False
      for o,a in self.opts:
        if o in [ "-C", '--'+options['C'][0] ]:
          self._coarray = True
    return self._coarray
  coarray = property(fget=coarray)

  def directives(self):
    if '_directives' not in self.__dict__:
      self._directives = True
      for o,a in self.opts:
        if o in [ "-r", '--'+options['r'][0] ]:
          self._directives = False
    return self._directives
  directives = property(fget=directives)

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
    print_options()
    print ""
    print "Version : ", version
    print ""

  def opts(self):
    if self._opts is None:
      optlist = ["",[]]
      for o in options:
        b = [o]+options[o]
        if b[3] == 1:
          b[0] = b[0]+":"
          b[1] = b[1]+"="
        optlist[0] += b[0]
        optlist[1] += [b[1]]
    
      try:
        self._opts, args = getopt.getopt(self.argv[1:], optlist[0], optlist[1])
      except getopt.GetoptError, err:
        # print help information and exit:
        self.usage()
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    
    return self._opts
  opts = property(fget=opts)
  
  t = """
def do_$LONG(self):
    if '_do_$LONG' not in self.__dict__:
      self._do_$LONG = False
      for o,a in self.opts:
        if o in ("-$SHORT", "--$LONG"):
          self._do_$LONG = True
          break
    return self._do_$LONG
do_$LONG = property(fget=do_$LONG)
"""
  for short in options:
    long = options[short][0]
    exec t.replace("$LONG",long).replace("$SHORT",short) #in locals()

  def do_run(self):
   if '_do_run' not in self.__dict__:
     self._do_run = not ( \
       self.do_version or \
       self.do_help    or \
       self.do_preprocess or \
       self.do_touch or \
       self.do_init )
   return self._do_run
  do_run = property(fget=do_run)


command_line = CommandLine()

def print_options():
  keys = options.keys()
  keys.sort()
  import subprocess, threading
  for k in keys:
    description = options[k][1]
    p1 = subprocess.Popen(["fold", "-s", "-w", "40"],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    description = p1.communicate(description)[0]
    description = description.replace('\n','\n'.ljust(27))
    print ("-%s, --%s"%(k,options[k][0])).ljust(25), description+'\n'

if __name__ == '__main__':
  print_options()
