#!/usr/bin/python

def modify_functions():
  result = []
  for filename,text in parsed_text:
    begin = -1
    for i, (vars,line) in enumerate(text):
      if type(line) in [ Subroutine, Function ]:
        text[i] = [ text[i] ]
        variable_list = list(vars)
        begin = i
      elif type(line) in [ End_provider, End ]:
        text[begin].insert(1,map(lambda x: ([],x), build_use(variable_list)))
      else:
        variable_list += vars
    text = flatten(text)
    result.append ( (filename, text) )

def residual_text():
  pass

