#!/usr/bin/python

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

if __name__ == '__main__':
  txt = open('/etc/passwd','r').readlines()
  print same_file('/etc/passwd',txt)
  print same_file('/etc/group',txt)
  print same_file('/etc/passwd-',txt)
