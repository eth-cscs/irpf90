#!/usr/bin/env python
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
  str="Empty_line"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Empty_line",self.i,self.text)

class Simple_line(Line):
  str="Simple_line"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Simple_line",self.i,self.text)

class Declaration(Line):
  str="Declaration"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Declaration",self.i,self.text)

class Continue(Line):
  str="Continue"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Continue",self.i,self.text)

class Begin_provider(Line):
  str="Begin_provider"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_provider",self.i,self.text)

class Cont_provider(Line):
  str="Cont_provider"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Cont_provider",self.i,self.text)

class End_provider(Line):
  str="End_provider"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_provider",self.i,self.text)

class Begin_doc(Line):
  str="Begin_doc"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_doc",self.i,self.text)

class Doc(Line):
  str="Doc"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Doc",self.i,self.text)

class End_doc(Line):
  str="End_doc"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_doc",self.i,self.text)

class Begin_shell(Line):
  str="Begin_shell"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_shell",self.i,self.text)

class End_shell(Line):
  str="End_shell"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_shell",self.i,self.text)

class Begin_template(Line):
  str="Begin_template"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_template",self.i,self.text)

class End_template(Line):
  str="End_template"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_template",self.i,self.text)

class Subst(Line):
  str="Subst"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Subst",self.i,self.text)

class Assert(Line):
  str="Assert"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Assert",self.i,self.text)

class Touch(Line):
  str="Touch"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Touch",self.i,self.text)

class SoftTouch(Touch):
  str="SoftTouch"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("SoftTouch",self.i,self.text)

class Irp_read(Line):
  str="Irp_read"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_read",self.i,self.text)

class Irp_write(Line):
  str="Irp_write"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_write",self.i,self.text)

class Irp_If(Line):
  str="Irp_If"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_If",self.i,self.text)

class Irp_Else(Line):
  str="Irp_Else"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_Else",self.i,self.text)

class Irp_Endif(Line):
  str="Irp_Endif"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_Endif",self.i,self.text)

class Openmp(Line):
  str="Openmp"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Openmp",self.i,self.text)

class Directive(Line):
  str="Directive"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Directive",self.i,self.text)

class Use(Line):
  str="Use"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Use",self.i,self.text)

class Do(Line):
  str="Do"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Do",self.i,self.text)

class Enddo (Line):
  str="Enddo"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Enddo",self.i,self.text)

class If(Line):
  str="If"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("If",self.i,self.text)

class Elseif(Line):
  str="Elseif"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Elseif",self.i,self.text)

class Else(Line):
  str="Else"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Else",self.i,self.text)

class Endif(Line):
  str="Endif"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Endif",self.i,self.text)

class Select(Line):
  str="Select"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Select",self.i,self.text)

class Case(Line):
  str="Case"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Case",self.i,self.text)

class End_select(Line):
  str="End_select"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_select",self.i,self.text)

class Program(Line):
  str="Program"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Program",self.i,self.text)

class Subroutine(Line):
  str="Subroutine"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Subroutine",self.i,self.text)

class Function(Line):
  str="Function"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Function",self.i,self.text)

class Call(Line):
  str="Call"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Call",self.i,self.text)

class Provide(Line):
  str="Provide"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Provide",self.i,self.text)

class NoDep(Line):
  str="NoDep"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("NoDep",self.i,self.text)

class Return (Line):
  str="Return"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Return",self.i,self.text)

class Include(Line):
  str="Include"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Include",self.i,self.text)

class Implicit (Line):
  str="Implicit"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Implicit",self.i,self.text)

class Free(Line):
  str="Free"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Free",self.i,self.text)

class End(Line):
  str="End"
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End",self.i,self.text)

class Provide_all (Line):
  str="Provide_all"
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
  for dir in command_line.include_dir:
    try:
      os.stat(dir)
      result += map(lambda x: dir+x, filter ( is_irpf90_file, os.listdir(dir) ) )
    except:
      continue
  if command_line.do_codelet:
    result += [command_line.codelet[3]]
  return result
irpf90_files = create_irpf90_files()




