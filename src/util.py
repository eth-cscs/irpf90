#!/usr/bin/python

def strip(x):
  return x.strip()

def lower(x):
  return x.lower()

def same_file(filename,txt):
  assert isinstance(filename,str)
  assert isinstance(txt,list)

  try:
    file = open(filename,"r")
  except IOError:
    return False
  lines = file.readlines()
  file.close()
  if len(lines) != len(txt):
    return False
  for a,b in zip(lines,txt):
    if a != b:
      return False
  return True

def build_dim(dim):
  if len(dim) == 0:
    return ""
  else:
    return "(%s)"%( ",".join(dim) )


def find_subname(line):
  buffer = line.text.split('(')
  if len(buffer) > 1:
    buffer = " ".join(buffer[:-1])
  else:
    buffer = buffer[0]
  buffer = buffer.lower().split()
  if len(buffer) < 2:
    error.fail(line,"Syntax Error")
  return buffer[-1]

def make_single(l):
  d = {}
  for x in l:
   d[x] = True
  return d.keys()

def flatten(l):
  if isinstance(l,list):
    result = []
    for i in range(len(l)):
      elem = l[i]
      result += flatten(elem)
    return result
  else:
    return [l]

if __name__ == '__main__':
  a = 0
  print flatten(a)
  a = []
  print flatten(a)
  a = [1,2,3,4]
  print flatten(a)
  a = [1,2,3,[4,5,6,[7,8,9],10,],11,12,[13,14],15,16]
  print flatten(a)
