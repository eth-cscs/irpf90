#!/usr/bin/python

from irpf90_t import *
from util import *
import error

class Variable(object):

  ############################################################
  def __init__(self,text,name = None):
    assert isinstance(text,list)
    assert len(text) > 0
    assert isinstance(text[0],Begin_provider)
    self.text = text
    if name is not None:
      self._name = name.lower()

  ############################################################
  def name(self):
    '''Name is lowercase'''
    if '_name' not in self.__dict__:
      buffer = None
      for line in self.text:
        if isinstance(line,Begin_provider):
          buffer = line.text.replace(']',',').split(',')
          break
      assert buffer is not None
      if len(buffer) < 3:
        error.fail(line, "Error in Begin_provider line")
      self._name = buffer[1].strip().lower()
    return self._name
  name = property(name)

  ############################################################
  def doc(self):
    if '_doc' not in self.__dict__:
      def f(l): return 
      buffer = filter(lambda l:isinstance(l,Doc), self.text)
      self._doc = map(lambda l: l.text[1:], buffer)
      if buffer == []:
        error.warn(None,"Variable %s is not documented"%(self.name))
    return self._doc
  doc = property(doc)

  ############################################################
  def others(self):
    if '_others' not in self.__dict__:
      result = []
      def f(l):
        return isinstance(l,Begin_provider) or isinstance(l,Cont_provider)
      lines = filter(f, self.text)
      for line in lines:
        buffer = line.text.replace(']',',').split(',')
        if len(buffer) < 3:
          error.fail(line,"Syntax Error") 
        buffer = buffer[1].strip().lower()
        result.append(buffer)
      result.remove(self.name)
      self._others = result
    return self._others
  others = property(others)

  ############################################################
  def same_as(self):
    if '_same_as' not in self.__dict__:
      if isinstance(self.line,Begin_provider):
        result = None
      else:
        buffer = self.text[0].text.replace(']',',').split(',')
        if len(buffer) < 3:
          error.fail(line,"Syntax Error")
        result = buffer[1].strip().lower()
      self._same_as = result
    return self._same_as
  same_as = property(same_as)

  ############################################################
  def allocate(self):
    if '_allocate' not in self.__dict__:
      from variables import variables
      def f(var):
        return variables[var].dim != []
      self._allocate = filter ( f, self.others + [self.name] )
    return self._allocate
  allocate = property(allocate)

  ############################################################
  def dim(self):
    if '_dim' not in self.__dict__:
      line = self.line.text
      buffer = line.replace(']','').split(',',2)
      if len(buffer) == 2:
        self._dim = []
      else:
        buffer = buffer[2].strip()[1:-1].split(',')
        self._dim = map(strip,buffer)
    return self._dim
  dim = property(dim)

  ############################################################
  def type(self):
    if '_type' not in self.__dict__:
      line = self.line.text
      buffer = line.split(',')[0]
      buffer = buffer.split('[')[1].strip()
      if self.dim != '':
        buffer = "%s, allocatable"%(buffer)
      self._type = buffer
    return self._type
  type = property(type)

  ############################################################
  def fmodule(self):
    if '_fmodule' not in self.__dict__:
      self._fmodule = self.line.filename.replace('.irp.f','_mod')
    return self._fmodule
  fmodule = property(fmodule)

  ############################################################
  def regexp(self):
    if '_regexp' not in self.__dict__:
      import re
      self._regexp = re.compile( \
        r"^.*[^a-z0-9'\"_]+%s([^a-z0-9_]|$)"%(self.name),re.I)
    return self._regexp
  regexp = property(regexp)

  ############################################################
  def line(self):
    if '_line' not in self.__dict__:
      def f(l):
        return isinstance(l,Begin_provider) or isinstance(l,Cont_provider)
      lines = filter(f, self.text)
      for line in lines:
        buffer = line.text.replace(']',',').split(',')
        if len(buffer) < 3:
          error.fail(line,"Syntax Error") 
        buffer = buffer[1].strip().lower()
        if self.name == buffer:
          self._line = line
          break
    assert '_line' in self.__dict__
    return self._line
  line = property(line)

  ############################################################
  def needs(self):
    if '_needs' not in self.__dict__:
      self._needs = None
    return self._needs
  needs = property(needs)

  ############################################################
  def header(self):
    if '_header' not in self.__dict__:
      name = self.name
      self._header = [
        "  %s :: %s %s"%(self.type, name, build_dim(self.dim) ),
        "  logical :: %s_is_built = .False."%(name),
      ]
    return self._header
  header = property(header)

######################################################################
if __name__ == '__main__':
  from preprocessed_text import preprocessed_text
  from variables import variables
  print variables['elec_fitcusp_lapl'].doc
