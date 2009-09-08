#!/usr/bin/python

from irpf90_t import *
from variable import *
from variables import variables

class Fmodule(object):

  def __init__(self,text,filename):
    self.text = text
    self.name = "%s_mod"%(filename[:-6].lower())

  def is_main(self):
    if '_is_main' not in self.__dict__:
      buffer = filter(lambda x: isinstance(x[1],Program),self.text)
      self._is_main = (buffer != [])
    return self._is_main
  is_main = property(is_main)

  def variables(self):
    if '_variables' not in self.__dict__:
      from variables import variables
      name = self.name
      self._variables = filter(lambda x: variables[x].fmodule == name, variables)
    return self._variables
  variables = property(variables)

  def head(self):
    if '_head' not in self.__dict__:
      self._head = None
    return self._head
  head = property(head)

  def needed_vars(self):
    if '_needed_vars' not in self.__dict__:
      result = map(lambda x: variables[x].needs,self.variables)
      result = make_single ( flatten(result) )
      self._needed_vars = result
    return self._needed_vars
  needed_vars = property(needed_vars)

  def generated_text(self):
    if '_generated_text' not in self.__dict__:
      self._generated_text = None
    return self._generated_text
  generated_text = property(generated_text)

  def residual_text(self):
    if '_residual_text' not in self.__dict__:
      self._residual_text = None
    return self._residual_text
  residual_text = property(residual_text)

  def needed_modules(self):
    if '_needed_modules' not in self.__dict__:
      buffer = filter(lambda x: isinstance(x,Use), self.generated_text)
      buffer = map(lambda x: x.text.split()[1].lower(), buffer)
      self._needed_modules = make_single(buffer)
    return self._needed_modules
  needed_modules = property(needed_modules)

if __name__ == '__main__':
  from parsed_text import parsed_text
  for filename, text in parsed_text:
    if filename == 'electrons.irp.f':
     x = Fmodule(text,filename)
     break
  print x.needed_vars
  print x.is_main

