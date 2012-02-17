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
from zlib import crc32

irpdir = "IRPF90_temp/"
mandir = "IRPF90_man/"
irp_id = abs(crc32(os.getcwd()))


class Line(object):
  def __init__(self,i,text,filename):
    self.i = i
    self._text = None
    self.filename = filename
    self._lower = None
    self.set_text(text)

  def get_text(self):
    return self._text
  
  def set_text(self,value):
    self._text = value
    self._lower = value.lower()

  def get_lower(self):
    return self._lower

  text = property(fget=get_text, fset=set_text)
  lower = property(fget=get_lower)

class Empty_line(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Empty_line",self.i,self.text)

class Simple_line(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Simple_line",self.i,self.text)

class Declaration(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Declaration",self.i,self.text)

class Continue(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Continue",self.i,self.text)

class Begin_provider(Line):
  str = "Provider"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_provider",self.i,self.text)

class Cont_provider(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Cont_provider",self.i,self.text)

class End_provider(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_provider",self.i,self.text)

class Begin_doc(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_doc",self.i,self.text)

class Doc(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Doc",self.i,self.text)

class End_doc(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_doc",self.i,self.text)

class Begin_shell(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_shell",self.i,self.text)

class End_shell(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_shell",self.i,self.text)

class Begin_template(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_template",self.i,self.text)

class End_template(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_template",self.i,self.text)

class Subst(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Subst",self.i,self.text)

class Assert(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Assert",self.i,self.text)

class Touch(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Touch",self.i,self.text)

class SoftTouch(Touch):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("SoftTouch",self.i,self.text)

class Irp_read(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_read",self.i,self.text)

class Irp_write(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_write",self.i,self.text)

class Irp_If(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_If",self.i,self.text)

class Irp_Else(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_Else",self.i,self.text)

class Irp_Endif(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_Endif",self.i,self.text)

class Openmp(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Openmp",self.i,self.text)

class Directive(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Directive",self.i,self.text)

class Use(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Use",self.i,self.text)

class Do(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Do",self.i,self.text)

class Enddo (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Enddo",self.i,self.text)

class If(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("If",self.i,self.text)

class Elseif(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Elseif",self.i,self.text)

class Else(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Else",self.i,self.text)

class Endif(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Endif",self.i,self.text)

class Select(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Select",self.i,self.text)

class Case(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Case",self.i,self.text)

class End_select(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_select",self.i,self.text)

class Program(Line):
  str = "Program"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Program",self.i,self.text)

class Subroutine(Line):
  str = "Subroutine"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Subroutine",self.i,self.text)

class Function(Line):
  str = "Function"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Function",self.i,self.text)

class Call(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Call",self.i,self.text)

class Provide(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Provide",self.i,self.text)

class NoDep(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("NoDep",self.i,self.text)

class Return (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Return",self.i,self.text)

class Include(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Include",self.i,self.text)

class Implicit (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Implicit",self.i,self.text)

class Free(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Free",self.i,self.text)

class End(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End",self.i,self.text)

class Provide_all (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Provide_all",self.i,self.text)


######################################################################

def create_irpf90_files():
  result = []
  from command_line import command_line
  import os
  def is_irpf90_file(filename):
    return filename.endswith(".irp.f") and not filename.startswith('.')
  result = filter ( is_irpf90_file, os.listdir(os.getcwd()) )
  return result
irpf90_files = create_irpf90_files()




