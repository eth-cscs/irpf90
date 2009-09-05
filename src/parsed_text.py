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
  buffer = line.text.split('(')[0]
  buffer = buffer.split()[1]
  return buffer

def check_touch(line,vars,main_vars):
  def fun(main_var):
    if main_var not in variables:
      error.fail(line,"Variable %s unknown"%(main_var,))
    x = variables[main_var]
    return [main_var]+x.others
  all_others = make_single(flatten( map(fun,main_vars) ))
  all_others.sort()
  if len(all_others) == len(vars):
    vars.sort()
    for x,y in zip(vars,all_others):
      if x != y:
        message = "The following entities should be touched:\n"
        message = "\n".join([message]+map(lambda x: "- %s"%(x,),all_others))
        error.fail(line,message)

def get_parsed_text():
  main_result = []
  for filename, text in preprocessed_text:
    result = []
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
        End_provider,
      ]: 
        result.append( ([],line) )
      elif isinstance(line,Provide):
        l = line.text.split()[1:]
        result.append( (l,Simple_line(line.i,"!%s"%(line.text),line.filename)) )
      elif isinstance(line,Call):
        sub = find_subroutine_in_line(line)
        if sub not in subroutines:
          t = Simple_line
        else:
          if subroutines[sub].touches == []:
            t = Simple_line
          else:
            t = Provide_all
        result.append( ([],t(line.i,line.text,line.filename)) )
      elif isinstance(line,Free):
        vars = line.text.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        vars = vars[1:]
        result.append( ([],Simple_line(line.i,"!%s"%(line.text),line.filename)) )
        for var in vars:
          result.append( ([],Simple_line(line.i,"  call free_%s"%var,
            line.filename)) )
      elif isinstance(line,Touch):
        vars = line.text.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        vars = map(lower,vars[1:])
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          main = variables[x].same_as
          if main is None:
            main = x
          return main
        main_vars = make_single( map(fun, vars) )
        check_touch(line,vars,main_vars)
        txt = " ".join(vars)
        result +=  [ ([],Simple_line(line.i,"!",line.filename)),
                    ([],Simple_line(line.i,"! >>> TOUCH %s"%(txt,),line.filename)) ]
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          return [ ([],Simple_line(line.i," call touch_%s"%(x,),line.filename)),
                   ([],Simple_line(line.i," %s_is_built = .True."%(x,),line.filename)) ]
        result += flatten(map( fun, main_vars ))
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          return ([],Simple_line(line.i," %s_is_built = .True."%(x,),line.filename))
        result += map( fun, main_vars[:-1] )
        result += [ ([],Provide_all(line.i,"! <<< END TOUCH",line.filename)) ]
      elif type(line) in [ Begin_provider, Cont_provider ]:
        buffer = map(strip,line.text.replace(']','').split(','))
        assert len(buffer) > 1
        v = buffer[1].lower()
        variable_list = find_variables_in_line(line)
        variable_list.remove(v)
        result.append( (variable_list,line) )
      else:
        l = find_variables_in_line(line)
        result.append( (l,line) )
    main_result.append( (filename, result) )
  return main_result

parsed_text = get_parsed_text()

if __name__ == '__main__':
   for line in parsed_text[12][1]:
     print line[1],'!',line[0]
