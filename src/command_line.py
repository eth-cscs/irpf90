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
options['d'] = [ 'debug'        , 'Activate debug', 0 ]
options['v'] = [ 'version'      , 'Print version of irpf90', 0 ]
options['a'] = [ 'assert'       , 'Activate assertions', 0 ]
options['h'] = [ 'help'         , 'Print this help', 0 ]
options['i'] = [ 'init'         , 'Initialize current directory', 0 ]
options['D'] = [ 'define'       , 'Define variable', 1 ]
options['o'] = [ 'checkopt'     , 'Show where optimization may be required', 0 ]
options['p'] = [ 'preprocess'   , 'Preprocess file', 1 ]
options['g'] = [ 'profile'      , 'Generate profile code', 0 ]
options['t'] = [ 'touch'        , 'Display which entities are touched', 1 ]
options['m'] = [ 'memory'       , 'Debug memory info', 0 ]
options['z'] = [ 'openmp'       , 'Automatic openMP tasks (may not work)', 0 ]
options['l'] = [ 'align'        , 'Align arrays using compiler directives. Sets the $IRP_ALIGN variable', 1 ]
options['s'] = [ 'substitute'   , 'Substitute values for loop max values', 1 ]
options['r'] = [ 'no_directives', 'Ignore compiler directives !DEC$ and !DIR$', 0 ]
options['n'] = [ 'inline'       , 'all|providers|builders : Force inlining of providers or builders', 1 ]

class CommandLine(object):

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
