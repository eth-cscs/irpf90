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
from variable import *
from variables import variables
from command_line import command_line
import preprocessed_text
from util import *

class Fmodule(object):

  header = \
     [ "! -*- F90 -*-",
       "!",
       "!-----------------------------------------------!",
       "! This file was generated with the irpf90 tool. !",
       "!                                               !",
       "!           DO NOT MODIFY IT BY HAND            !",
       "!-----------------------------------------------!",
       "" ]

  def __init__(self,text,filename):
    self.text = put_info(text,filename)
    self.name = "%s_mod"%(filename[:-6])

  def is_main(self):
    if '_is_main' not in self.__dict__:
      self._is_main = self.prog_name is not None
    return self._is_main
  is_main = property(is_main)

  def prog_name(self):
    if '_prog_name' not in self.__dict__:
      buffer = filter(lambda x: type(x[1]) == Program,self.text)
      if buffer == []:
        self._prog_name = None
      else:
        self._prog_name = buffer[0][1].filename
    return self._prog_name
  prog_name = property(prog_name)

  def variables(self):
    if '_variables' not in self.__dict__:
      from variables import variables
      name = self.name
      self._variables = filter(lambda x: variables[x].fmodule == name, variables)
    return self._variables
  variables = property(variables)


  def head(self):
    if '_head' not in self.__dict__:
      result = [ "module %s"%(self.name) ]
      result += self.use
      result += self.dec
      result += flatten( map(lambda x: variables[x].header,self.variables) )
      result.append( "end module %s"%(self.name) )
      self._head = result
    return self._head
  head = property(head)

  def needed_vars(self):
    if '_needed_vars' not in self.__dict__:
      result = map(lambda x: variables[x].needs,self.variables)
      result = make_single ( flatten(result) )
      self._needed_vars = result
    return self._needed_vars
  needed_vars = property(needed_vars)

  def includes(self):
    if '_includes' not in self.__dict__:
      buffer = []
      for v in self.needed_vars:
        buffer += variables[v].includes
      self._includes = make_single(buffer)
    return self._includes
  includes = property(includes)

  def generated_text(self):
    if '_generated_text' not in self.__dict__:
      result = []
      for var in self.variables:
        var = variables[var]
        result += var.provider
        result += var.builder
        if var.is_read:
          result += var.reader
        if var.is_written:
          result += var.writer
      self._generated_text = result
    return self._generated_text
  generated_text = property(generated_text)

  def residual_text(self):
    if '_residual_text' not in self.__dict__:
      from variables import build_use, call_provides
      from parsed_text import move_to_top
      def remove_providers(text):
        result = []
        inside = False
        for vars,line in text:
          if type(line) == Begin_provider:
            inside = True
          if not inside:
            result.append( (vars,line) )
          if type(line) == End_provider:
            inside = False
        return result

      def modify_functions(text):
        result = []
        variable_list = []
        for vars,line in text:
          if type(line) in [ Subroutine, Function ]:
            variable_list = list(vars)
          elif type(line) == End:
            result += map(lambda x: ([],Use(line.i,x,line.filename)), build_use(variable_list))
          else:
            variable_list += vars
          result.append( (vars,line) )
        return result

      def extract_use_dec_text(text):
        inside = False
        result = []
        dec = []
        use = []
        for vars,line in text:
          if type(line) in [ Subroutine, Function, Program]:
            inside = True
          if inside:
            result.append( (vars,line) )
          else:
            if type(line) == Use:
              use.append( (vars,line) )
            elif type(line) == Declaration:
              dec.append( (vars,line) )
          if type(line) == End:
            inside = False
        return use, dec, result

      def provide_variables(text):
        result = []
        for vars,line in text:
          result.append( ([],line) )
          result += map(lambda x: ([],Simple_line(line.i,x,line.filename)), call_provides(vars)) 
        return result

      result = remove_providers(self.text)
      result = modify_functions(result)
      use,dec,result = extract_use_dec_text(result)
      self._use = make_single(map(lambda x: " "+x[1].text, use))
      self._dec = make_single(map(lambda x: " "+x[1].text, dec))
      result = provide_variables(result)
      result = move_to_top(result,Declaration)
      result = move_to_top(result,Implicit)
      result = move_to_top(result,Use)
      result    = map(lambda x: x[1], result)
      result    = map(lambda x: x.text, result)
      self._residual_text = result
    return self._residual_text
  residual_text = property(residual_text)

  def use(self):
    if '_use' not in self.__dict__:
      self.residual_text
    return self._use
  use = property(use)

  def dec(self):
    if '_dec' not in self.__dict__:
      self.residual_text
    return self._dec
  dec = property(dec)


  def needed_modules(self):
    if '_needed_modules' not in self.__dict__:
      buffer = filter(lambda x: x.lstrip().startswith("use "), \
        self.generated_text+self.head+self.residual_text)
      buffer = map(lambda x: x.split()[1], buffer)
      buffer = filter(lambda x: x.endswith("_mod"),buffer )
      self._needed_modules = make_single(buffer)
      if self.name in self._needed_modules:
        self._needed_modules.remove(self.name)
    return self._needed_modules
  needed_modules = property(needed_modules)

######################################################################

if __name__ == '__main__':
  from parsed_text import parsed_text
  for filename, text in parsed_text:
    if filename == 'vmc_step.irp.f':
     x = Fmodule(text,filename)
     break
  for line in x.head:
    print line
  print x.includes

