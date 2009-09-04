#!/usr/bin/python

from subroutine import *
from irpf90_t import *

def create_subroutines():
  from preprocessed_text import preprocessed_text
  result = {}
  for filename, text in preprocessed_text:
    buffer = []
    inside = False
    for line in text:
      if isinstance(line,Subroutine):
        inside = True
      if inside:
        buffer.append(line)
      if isinstance(line,End):
        if inside:
         v = Sub(buffer)
         result[v.name] = v
         buffer = []
        inside = False
  return result

subroutines = create_subroutines()

if __name__ == '__main__':
  for v in subroutines.keys():
    print v
