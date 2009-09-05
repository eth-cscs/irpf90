#!/usr/bin/python

from util import *
from irpf90_t import *
from variables import variables
from preprocessed_text import preprocessed_text
from subroutines import subroutines
import regexps
import error

def find_variables_in_line(line):
  assert isinstance(line,Line)
  result = []
  buffer = regexps.re_string.sub('',line.text)
  for v in variables.keys():
    var = variables[v]
    if var.regexp.search(buffer) is not None:
      result.append(var.name)
  return result

def find_subroutine_in_line(line):
  assert isinstance(line,Call)
  buffer = regexps.re_string.sub('',line.text)
  result = None
  for v in subroutines.keys():
    sub = subroutines[v]
    if sub.regexp.search(buffer) is not None:
      result = sub.name
      break
  assert result is not None
  return result

def check_touch(vars,main_vars):
  def fun(main_var):
    if main_var not in variables:
      error.fail(line,"Variable %s unknown"%(main_var,))
    x = variables[main_var]
    return [main_var]+x.others
  all_others = flatten( map(fun,main_vars) )
  all_others.sort()
  if len(all_others) == len(vars):
    for x,y in zip(vars,all_others):
      if x != y:
        message = "The following entities should be touched:\n"
        message = "\n".join([message]+map(lambda x: "- %s"%(x,),all_others))
        error.fail(line,message)

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
        temp_result.append( (l,Simple_line(line.i,"!%s"%(line.text),line.filename)) )
      elif isinstance(line,Call):
        sub = find_subroutine_in_line(line)
        if subroutines[sub].touches == []:
          t = Simple_line
        else:
          t = Provide_all
        temp_result.append( ([],t(line.i,line.text,line.filename)) )
      elif isinstance(line,Free):
        vars = line.text.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        vars = vars[1:]
        result.append( ([],Simple_line(line.i,"!%s"%(line.text),line.filename)) )
        for var in vars:
          temp_result.append( ([],Simple_line(line.i,"  call free_%s"%var,
            line.filename)) )
      elif isinstance(line,Touch):
        vars = line.text.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        vars = vars[1:]
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          main = variables[x].same_as
          if main is None:
            main = x
          return main
        main_vars = make_single( map(fun, vars) )
        check_touch(vars,main_vars)
        txt = " ".join(vars)
        result =  [ ([],Simple_line(line.i,"!",line.filename)),
                    ([],Simple_line(line.i,"! >>> TOUCH %s"%(txt,),line.filename)) ]
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          return [ ([],Simple_line(line.i," call touch_%s"%(x,),line.filename)),
                   ([],Simple_line(line.i," %s_is_built = .True."%(x,),line.filename)) ]
        result += map( fun, main_vars )
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          return [ ([],Simple_line(line.i," %s_is_built = .True."%(x,),line.filename)) ]
        result += map( fun, main_vars )
        result += [ ([],Provide_all(line.i,"! <<< END TOUCH",line.filename)) ]
      else:
        l = find_variables_in_line(line)
        varlist += l
        temp_result.append( (l,line) )
    result.append( (filename, temp_result) )
  return result

parsed_text = get_parsed_text()

if __name__ == '__main__':
   for line in parsed_text[0][1]:
     print line
