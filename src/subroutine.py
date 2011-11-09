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
from util import *
import error

class Sub(object):

  ############################################################
  def __init__(self,text):
    assert type(text) == list
    assert len(text) > 0
    assert type(text[0]) in [Subroutine, Function]
    self.text = text

  ############################################################
  def name(self):
    '''Name is lowercase'''
    if '_name' not in self.__dict__:
      self._name = find_subname(self.line)
    return self._name
  name = property(name)

  ############################################################
  def is_function(self):
    if '_is_function' not in self.__dict__:
      self._is_function = "function" in self.line.lower
    return self._is_function
  is_function = property(is_function)

  ############################################################
  def doc(self):
    if '_doc' not in self.__dict__:
      def f(l): return 
      buffer = filter(lambda l:type(l) == Doc, self.text)
      self._doc = map(lambda l: l.text[1:], buffer)
      if buffer == []:
        error.warn(None,"Subroutine %s is not documented"%(self.name))
    return self._doc
  doc = property(doc)

  ############################################################
  def line(self):
    if '_line' not in self.__dict__:
      self._line = self.text[0]
    return self._line
  line = property(line)

  ############################################################
  def touches(self):
    if '_touches' not in self.__dict__:
      from subroutines import subroutines
      self._touches = []
      for line in filter(lambda x: type(x) in [Touch, SoftTouch],self.text):
        self._touches += line.text.split()[1:]
      for sub in self.calls:
        if sub in subroutines:
          self._touches += subroutines[sub].touches
      self._touches = make_single(self._touches)
    return self._touches
  touches = property(touches)

  ############################################################
  def needs(self):
    if '_needs' not in self.__dict__:
      import parsed_text
    return self._needs
  needs = property(needs)

  ############################################################
  def to_provide(self):
    if '_to_provide' not in self.__dict__:
      import parsed_text
    return self._to_provide
  to_provide = property(to_provide)

  ############################################################
  def regexp(self):
    if '_regexp' not in self.__dict__:
      import re
      self._regexp = re.compile( \
        r"([^a-z0-9'\"_]|^)%s([^a-z0-9_]|$)"%(self.name),re.I)
    return self._regexp
  regexp = property(regexp)

  ############################################################
  def calls(self):
    if '_calls' not in self.__dict__:
      buffer = filter(lambda x: type(x) == Call,self.text)
      self._calls = []
      for line in buffer:
        sub = line.text.split('(',1)[0].split()[1]
        self._calls.append(sub)
      self._calls = make_single(self._calls)
    return self._calls
  calls = property(calls)

######################################################################
if __name__ == '__main__':
  from preprocessed_text import preprocessed_text
  from subroutines import subroutines
  print subroutines['run'].needs
  print subroutines['run'].to_provide
