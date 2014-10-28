#!/usr/bin/env python

import sys
import re

LENMAX = 70
tabn = 2
tab = " "*tabn

class Grep(object):

  re_begin_program = re.compile(r"^\s*program\s",flags=re.I)
  def begin_program(self,string):
    return re.match(self.re_begin_program,string) is not None

  re_end_program = re.compile(r"\s*(end\s*!?$|end\s*program)",flags=re.I)
  def end_program(self,string):
    return re.match(self.re_end_program,string) is not None

  re_begin_subroutine = re.compile(r"^\s*(recursive)?\s*subroutine\s",flags=re.I)
  def begin_subroutine(self,string):
    return re.match(self.re_begin_subroutine,string) is not None

  re_end_subroutine = re.compile(r"\s*(end\s*!?$|end\s*subroutine)",flags=re.I)
  def end_subroutine(self,string):
    return re.match(self.re_end_subroutine,string) is not None

  re_begin_function = re.compile(r"^.*function\s+.*\(",flags=re.I)
  def begin_function(self,string):
    return re.match(self.re_begin_function,string) is not None

  re_end_function = re.compile(r"\s*(end\s*!?$|end\s*function)",flags=re.I)
  def end_function(self,string):
    return re.match(self.re_end_function,string) is not None

  re_begin_provider = re.compile(r"^\s*&?begin_provider\s",flags=re.I)
  def begin_provider(self,string):
    return re.match(self.re_begin_provider,string) is not None

  re_end_provider = re.compile(r"^\s*end_provider\s*(!.*)?$", flags=re.I)
  def end_provider(self,string):
    return re.match(self.re_end_provider,string) is not None

  re_begin_do = re.compile(r"^\s*do\s+",flags=re.I)
  def begin_do(self,string):
    return re.match(self.re_begin_do,string) is not None

  re_end_do = re.compile(r"^\s*end\s*do\s*(!.*)?$",flags=re.I)
  def end_do(self,string):
    return re.match(self.re_end_do,string) is not None

  re_begin_if = re.compile(r"^\s*if(\(|\s+).*(&|then)\s*(!.*)?$",flags=re.I)
  def begin_if(self,string):
    return re.match(self.re_begin_if,string) is not None

  re_else = re.compile(r"^\s*else",flags=re.I)
  def xelse(self,string):
    return re.match(self.re_else,string) is not None

  re_end_if = re.compile(r"^\s*end\s*if\s*(!.*)?$",flags=re.I)
  def end_if(self,string):
    return re.match(self.re_end_if,string) is not None

  re_begin_select = re.compile(r"^\s*select\s*case",flags=re.I)
  def begin_select(self,string):
    return re.match(self.re_begin_select,string) is not None

  re_case = re.compile(r"^\s*case\s*\(",flags=re.I)
  def case(self,string):
    return re.match(self.re_case,string) is not None

  re_end_select = re.compile(r"^\s*end\s*select\s*(!.*)?$",flags=re.I)
  def end_select(self,string):
    return re.match(self.re_end_select,string) is not None

  re_continuation = re.compile(r"^\s*\S+.*&")
  def continuation(self,string):
    return re.match(self.re_continuation,string) is not None

  re_declaration = re.compile(r"^.*::.*$")
  def declaration(self,string):
    return re.match(self.re_declaration,string) is not None

grep = Grep()

class indent(object):

  def __init__(self):
    """Run the program"""
    self.run()

  def format_declaration(self,string,n):
    l,r = string.split('::')
    return l.strip().ljust(n) + ' :: '+ r.strip()

  def format_continuation(self,string,n):
    buffer = string.split('&')
    if len(buffer) == 1:
      l = buffer[0]
      return l
    else:
      l, r = buffer
    return l.strip().ljust(69-len(n)) + '&'+ r.strip()

  def get_filename(self):
    """The file name is the first argument"""
    if '_filename' not in self.__dict__:
      try:
        self._filename = sys.argv[1]
      except:
        self._filename = None
    return self._filename
  filename=property(fget=get_filename)

  def get_text(self):
    """The text of the file is a list of lines"""
    if '_text' not in self.__dict__:
      if self.filename is not None:
        f = open(self.filename,'r')
        self._text = f.read().splitlines()
        f.close()
      else:
        self._text = sys.stdin.read().splitlines()
    return self._text
  text=property(fget=get_text)

  def indentlevel(self,line):
    line = line.rstrip()
    k=0
    if len(line) > 0:
      while line[k] == ' ':
        k+=1
    return k

  def run(self):
    lines = self.text
    indent0 = " "*self.indentlevel(self.text[0])
    k = indent0
    line = ""
    for i in range(len(self.text)):
      prevline = line
      line = self.text[i].strip()
      if grep.continuation(line):
        line = self.format_continuation(line,k)

      if grep.continuation(prevline):
        print k+2*tab+self.format_continuation(line,k+2*tab)
        continue

      if grep.begin_subroutine(line):
        print line
        k = indent0+tab
        continue

      if grep.begin_function(line):
        print line
        k = indent0+tab
        continue

      if grep.begin_program(line):
        print line
        k = indent0+tab
        continue

      if grep.begin_provider(line):
        if line[0] != '&':
          k = indent0+tab
          if grep.begin_provider(self.text[i+1].strip()):
            print " "+line
          else:
            print line
        else:
          print line
        continue

      if grep.declaration(line):
        print k+self.format_declaration(line,30)
        continue

      if grep.begin_do(line):
        print k+line
        k += tab
        continue

      if grep.begin_if(line):
        print k+line
        k += tab
        continue

      if grep.xelse(line):
        print k[:-tabn]+line
        continue

      if grep.begin_select(line):
        print k+line
        k += 2*tab
        continue

      if grep.case(line):
        print k[:-tabn]+line
        continue

      if grep.end_do(line):
        k = k[:-tabn]
        print k+line
        continue

      if grep.end_if(line):
        k = k[:-tabn]
        print k+line
        continue

      if grep.end_select(line):
        k = k[:-2*tabn]
        print k+line
        continue

      if grep.end_subroutine(line):
        print line
        k = indent0
        continue

      if grep.end_function(line):
        print line
        k = indent0
        continue

      if grep.end_provider(line):
        print line
        k = indent0
        continue

      if grep.end_program(line):
        print line
        k = indent0
        continue

      print k+line


def main():
  indent()


if __name__ == '__main__':
  main()

