#!/usr/bin/python

def strip(x):
  return x.strip()

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


if __name__ == '__main__':
  print build_dim([])
  print build_dim(['a'])
  print build_dim(['a','b'])
