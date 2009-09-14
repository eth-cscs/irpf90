#!/usr/bin/python

from variable import *
from irpf90_t import *
from util import *

######################################################################
def create_variables():
  from preprocessed_text import preprocessed_text
  result = {}
  for filename, text in preprocessed_text:
    buffer = []
    inside = False
    for line in text:
      if isinstance(line,Begin_provider):
        inside = True
      if inside:
        buffer.append(line)
      if isinstance(line,End_provider):
        inside = False
        v = Variable(buffer)
        result[v.name] = v
        for other in v.others:
          result[other] = Variable(buffer,other)
        buffer = []
  return result

variables = create_variables()

######################################################################
def build_use(vars):
  result = map(lambda x: "  use %s"%(variables[x].fmodule), vars)
  result = make_single(result)
  return result

######################################################################
def call_provides(vars,opt=False):
  vars = make_single( map(lambda x: variables[x].same_as, vars) )
  if opt:
    all_children = flatten( map(lambda x: variables[x].children, vars ))
    vars = filter(lambda x: x not in all_children,vars)
  def fun(x):
    return [ \
    "  if (.not.%s_is_built) then"%(x),
    "    call provide_%s"%(x),
    "  endif" ]
  return flatten ( map (fun, vars) )

######################################################################
if __name__ == '__main__':
  for v in variables.keys():
    print v
