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


from subroutine import *
from irpf90_t import *

def create_subroutines():
  from preprocessed_text import preprocessed_text
  result = {}
  for filename, text in preprocessed_text:
    buffer = []
    inside = False
    for line in text:
      if type(line) in [ Subroutine, Function ]:
        inside = True
      if inside:
        buffer.append(line)
      if isinstance(line,End):
        if inside:
         v = Sub(buffer)
         result[v.name] = v
         buffer = []
        inside = False
  return result

subroutines = create_subroutines()

if __name__ == '__main__':
  for v in subroutines.keys():
    print v
