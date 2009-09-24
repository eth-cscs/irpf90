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

