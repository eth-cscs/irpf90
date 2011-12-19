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



import vim
import os,sys
try:
  wd = os.path.abspath(os.path.dirname(__file__))
  sys.path.insert(0,(wd+"/../src/"))
except:
  pass
sys.setcheckinterval(1000)

def main():
  from command_line import command_line

  vim.install()

  if command_line.do_help:
    command_line.usage()

  if command_line.do_version:
    from version import version
    print version

  from init import init
  if command_line.do_init:
    init()

  if command_line.do_preprocess:
    init()
    from preprocessed_text import preprocessed_text
    for filename,text in preprocessed_text:
      if filename in command_line.preprocessed:
        for line in text:
          print line.text


  if command_line.do_touch:
    from variables import variables
    for var in command_line.touched:
      if var not in variables:
        print "%s is not an IRP entity"%(var,)
      else:
        print "%s touches the following entities:"%(var,)
        parents = variables[var].parents
        parents.sort()
        for x in parents:
          print "- %s"%(x,)

  if not command_line.do_run:
    return


  init()

  import irp_stack
  irp_stack.create()

  import makefile
  makefile.create()

  from modules import modules, write_module
  for m in modules.keys():
    write_module(modules[m])

  makefile.run()

  import touches
  touches.create()

  import create_man
  create_man.run()

  if command_line.do_profile:
    import profile
    profile.run()

if __name__ == '__main__':
  main()
