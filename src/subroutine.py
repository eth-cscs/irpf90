#!/usr/bin/python

from irpf90_t import *
from util import *
import error

class Sub(object):

  ############################################################
  def __init__(self,text):
    assert isinstance(text,list)
    assert len(text) > 0
    assert isinstance(text[0],Subroutine) or isinstance(text[0],Function)
    self.text = text

  ############################################################
  def name(self):
    '''Name is lowercase'''
    if '_name' not in self.__dict__:
      self._name = find_subname(self.line)
    return self._name
  name = property(name)

  ############################################################
  def doc(self):
    if '_doc' not in self.__dict__:
      def f(l): return 
      buffer = filter(lambda l:isinstance(l,Doc), self.text)
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
      for line in filter(lambda x: isinstance(x,Touch),self.text):
        self._touches += line.text.split()[1:]
      for sub in self.calls:
        self._touches += subroutines[sub].touches
      self._touches = make_single(self._touches)
    return self._touches
  touches = property(touches)

  ############################################################
  def regexp(self):
    if '_regexp' not in self.__dict__:
      import re
      self._regexp = re.compile( \
        r"^.*[^a-z0-9'\"_]+%s([^a-z0-9_]|$)"%(self.name),re.I)
    return self._regexp
  regexp = property(regexp)

  ############################################################
  def calls(self):
    if '_calls' not in self.__dict__:
      buffer = filter(lambda x: isinstance(x,Call),self.text)
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
  print subroutines['brownian_step'].touches
