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
  # Module data
  filename = irpdir+m.name[0:-4]+".irp.module.F90"
  text = m.header + m.head 
  text = map(lambda x: "%s\n"%(x),text)
  if not same_file(filename,text):
    print filename
    file = open(filename,"w")
    file.writelines(text)
    file.close()

  # Subroutines
  filename = irpdir+m.name[0:-4]+".irp.F90"
  text = m.header + m.generated_text + m.residual_text
  text = map(lambda x: "%s\n"%(x),text)
  if not same_file(filename,text):
    print filename
    file = open(filename,"w")
    file.writelines(text)
    file.close()

######################################################################
if __name__ == '__main__':
  write_module(modules['psi.irp.f'])
  

