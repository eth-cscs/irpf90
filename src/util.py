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

def dimsize(x):
  assert isinstance(x,str)
  buffer = x.split(':')
  if len(buffer) == 1:
    return x
    buffer = map(strip,buffer)
  else:
    assert len(buffer) == 2
    size = ""
    b0, b1 = buffer
    if b0.replace('-','').isdigit() and b1.replace('-','').isdigit():
      size = str( int(b1) - int(b0) + 1 )
    else:
      if b0.replace('-','').isdigit():
        size = "%s - (%d)"%(b1,int(b0)-1)
      elif b1.replace('-','').isdigit():
        size = "%d - %s"%(int(b1)+1,b0)
      else:
        size = "%s - %s + 1"%(b1,b0)
    return size

if __name__ == '__main__':
  print "10",dimsize("10") #-> "10"
  print "0:10",dimsize("0:10") # -> "11"
  print "0:x",dimsize("0:x")  # -> "x+1"
  print "-3:x",dimsize("-3:x")  # -> "x+1"
  print "x:y",dimsize("x:y")  # -> "y-x+1"
  print "x:5",dimsize("x:5")  # -> "y-x+1"

