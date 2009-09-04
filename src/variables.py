#!/usr/bin/python

from variable import *
from irpf90_t import *

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

if __name__ == '__main__':
  for v in variables.keys():
    print v
