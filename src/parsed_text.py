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
  varlist = []
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
      ]: 
        result.append( ([],line) )
      elif isinstance(line,End_provider):
        varlist = []
        result.append( ([],line) )
      elif isinstance(line,Provide):
        l = line.text.lower().split()[1:]
        l = filter(lambda x: x not in varlist, l)
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
        if isinstance(line,Begin_provider):
          varlist = []
        buffer = map(strip,line.text.replace(']','').split(','))
        assert len(buffer) > 1
        v = buffer[1].lower()
        varlist.append(v)
        variable_list = find_variables_in_line(line)
        variable_list.remove(v)
        result.append( (variable_list,line) )
      else:
        l = find_variables_in_line(line)
        l = filter(lambda x: x not in varlist, l)
        result.append( (l,line) )
    main_result.append( (filename, result) )
  return main_result

parsed_text = get_parsed_text()
######################################################################
def move_variables():

  main_result = []
  for filename, text in parsed_text:
    result = []
    # 1st pass
    varlist = []
    ifvars = []
    elsevars = []
    old_varlist = []
    old_ifvars = []
    old_elsevars = []
    revtext = list(text)
    revtext.reverse()
    for vars,line in revtext:
      if type(line) in [ End_provider,End ]:
        varlist = []
        result.append( ([],line) )
      elif type(line) in [ Endif, End_select ]:
        old_ifvars.append(ifvars)
        old_elsevars.append(elsevars)
        old_varlist.append(varlist)
        varlist = []
        result.append( ([],line) )
      elif type(line) == Else:
        result.append( (varlist,line) )
        elsevars = list(varlist)
        if vars != []:
          varlist = old_varlist.pop()
          varlist += vars
          old_varlist.append(varlist)
        varlist = []
      elif type(line) in [ Elseif, Case ]:
        ifvars += varlist
        result.append( (varlist,line) )
        if vars != []:
          varlist = old_varlist.pop()
          varlist += vars
          old_varlist.append(varlist)
        varlist = []
      elif type(line) in [ If, Select ]:
        ifvars += varlist
        result.append( (varlist,line) )
        vars += filter(lambda x: x in elsevars, ifvars)
        ifvars = old_ifvars.pop()
        elsevars = old_elsevars.pop()
        varlist = old_varlist.pop()
        varlist += vars
      elif type(line) in [ Begin_provider, Subroutine, Function ]:
        varlist += vars
        result.append( (varlist,line) )
        assert old_varlist == []
        assert old_ifvars == []
        assert old_elsevars == []
        varlist = []
      else:
        varlist += vars
        result.append( ([],line) )
    result.reverse()
    # 2nd pass
    text = result
    result = []
    old_varlist = []
    varlist = []
    for vars,line in text:
      if vars != []:
        vars = make_single(vars)
      if type(line) in [ Begin_provider, Subroutine, Function ]:
        varlist = list(vars)
      elif type(line) in [ If, Select ]:
        old_varlist.append(varlist)
        vars = filter(lambda x: x not in varlist,vars)
        varlist = make_single(varlist + vars)
        assert old_varlist is not varlist
      elif type(line) in [ Elseif, Else, Case ]:
        varlist = old_varlist.pop()
        old_varlist.append(varlist)
        vars = filter(lambda x: x not in varlist,vars)
        varlist = make_single(varlist + vars)
        assert old_varlist is not varlist
      elif type(line) in [ Endif, End_select ]:
        varlist = old_varlist.pop()
      elif type(line) == Provide_all:
        vars = varlist
      elif type(line) in [ End_provider, End ]:
        assert old_varlist == []
        varlist = []
      result.append( (vars,line) )

    main_result.append( (filename, result) )
  return main_result

parsed_text = move_variables()

######################################################################
def build_needs():
  # Needs
  for filename, text in parsed_text:
    for vars,line in text:
      if isinstance(line,Begin_provider):
        buffer = map(strip,line.text.replace(']',',').split(','))
        var = variables[buffer[1].lower()]
        var.needs = []
        var.to_provide = vars
      elif isinstance(line,End_provider):
        var.needs = make_single(var.needs)
        var.to_provide = make_single(var.to_provide)
        var = None
      if var is not None:
        var.needs += vars
  for v in variables.keys():
    main = variables[v].same_as 
    if main != v:
      variables[v].needs = variables[main].needs
      variables[v].to_provide = variables[main].to_provide

  # Needed_by
  for v in variables.keys():
    variables[v].needed_by = []
  for v in variables.keys():
    main = variables[v].same_as 
    if main != v:
      variables[v].needed_by = variables[main].needed_by
  for v in variables.keys():
    var = variables[v]
    for x in var.needs:
      variables[x].needed_by.append(var.same_as)
  for v in variables.keys():
    var = variables[v]
    var.needed_by = make_single(var.needed_by)


build_needs()

######################################################################
def put_info():
  for filename, text in parsed_text:
    if len(text) > 0:
      lenmax = 80 - len(text[0][1].filename)
      format = "%"+str(lenmax)+"s ! %s:%4s"
    for vars,line in text:
      line.text = format%(line.text.ljust(lenmax),line.filename,str(line.i))

######################################################################
if __name__ == '__main__':
 for i in range(len(parsed_text)):
   print '!-------- %s -----------'%(parsed_text[i][0])
   for line in parsed_text[i][1]:
     print line[1]
     print line[0]

