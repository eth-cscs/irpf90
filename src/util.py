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

if __name__ == '__main__':
  print build_dim([])
  print build_dim(['a'])
  print build_dim(['a','b'])
