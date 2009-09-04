#!/usr/bin/python

from util import *
from irpf90_t import *
from variables import variables
from preprocessed_text import preprocessed_text
from subroutines import subroutines
import regexps

def find_variables_in_line(line):
  assert isinstance(line,Line)
  result = []
  buffer = regexps.re_string.sub('',line.text)
  for v in variables.keys():
    var = variables[v]
    if var.regexp.search(buffer) is not None:
      result.append(var.name)
  return result


def get_parsed_text():
  result = []
  for filename, text in preprocessed_text:
    temp_result = []
    varlist = []
    for line in filter(
      lambda x: type(x) not in [ Doc, Begin_doc, End_doc ],
      text):
      if type(line) in [ \
        Empty_line,
        Continue,
        Return,
        Begin_shell,
        End_shell,
        Openmp,
        Use,
        Enddo,
        End_select,
        Endif,
        Implicit,
        Program,
        Subroutine,
        Function,
        End,
      ]: 
        temp_result.append( ([],line) )
      elif type(line) in [End, End_provider]:
        temp_result.append( ([],line) )
        varlist = []
      elif isinstance(line,Provide):
        l = line.text.split()[1:]
        varlist += l
        temp_result.append( (l,line) )
      else:
        l = find_variables_in_line(line)
        varlist += l
        temp_result.append( (l,line) )
    result.append( (filename, temp_result) )

parsed_text = get_parsed_text()

if __name__ == '__main__':
   for line in parsed_text[0][1]:
     print line
