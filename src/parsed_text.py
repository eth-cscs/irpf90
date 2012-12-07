#!/usr/bin/python
#   IRPF90 is a Fortran90 preprocessor written in Python for programming using
#   the Implicit Reference to Parameters (IRP) method.
#   Copyright (C) 2009 Anthony SCEMAMA 
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   Anthony Scemama
#   LCPQ - IRSAMC - CNRS
#   Universite Paul Sabatier
#   118, route de Narbonne      
#   31062 Toulouse Cedex 4      
#   scemama@irsamc.ups-tlse.fr


from util import *
from irpf90_t import *
from variables import variables
from preprocessed_text import preprocessed_text
from subroutines import subroutines
import regexps, re
import error

vtuple = map(lambda v: (v, variables[v].same_as, variables[v].regexp), variables.keys())
stuple = map(lambda s: (s, subroutines[s].regexp), subroutines.keys())
stuple = filter(lambda s: subroutines[s[0]].is_function, stuple)
re_string_sub = regexps.re_string.sub

regexps_re_string_sub = regexps.re_string.sub
def find_variables_in_line(line):
  assert isinstance(line,Line)
  result = []
  sub_done = False
  buffer = line.lower
  ap = result.append
  for v,same_as,regexp in vtuple:
    if v in buffer:
      if not sub_done:
        buffer = regexps_re_string_sub('',buffer)
        sub_done = True
      if regexp.search(buffer) is not None:
        ap(same_as)
  return result

def find_funcs_in_line(line):
  assert isinstance(line,Line)
  result = []
  append = result.append
  sub_done = False
  buffer = line.lower
  for s,regexp in stuple:
     if s in buffer:
      if regexp.search(buffer) is not None:
        append(s)
  return result


def find_subroutine_in_line(line):
  assert type(line) == Call
  buffer = line.text.split('(')[0]
  buffer = buffer.split()[1].lower()
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

################################################################################
def update_variables():
  for filename,text in preprocessed_text:

    for line in filter(lambda x: type(x) in [ Touch, SoftTouch ], text):
        vars = line.lower.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        for v in vars[1:]:
          if v not in variables:
            error.fail(line,"Variable %s unknown"%(v,))
          variables[v]._is_touched = True

    for line in filter(lambda x: type(x) == Free,text):
        vars = line.lower.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        for v in vars[1:]:
          if v not in variables:
            error.fail(line,"Variable %s unknown"%(v,))
          variables[v].is_freed = True

    for line in filter(lambda x: type(x) == Irp_read,text):
        variables[line.filename]._is_read = True

    for line in filter(lambda x: type (x) == Irp_write,text):
        variables[line.filename]._is_written = True

################################################################################
  
def get_parsed_text():
  def func(filename, text):
    varlist = []
    result = []
    append = result.append
    for line in text: #filter(
#     lambda x: type(x) not in [ Doc, Begin_doc, End_doc ],
#     text):
      if type(line) in [ \
        Empty_line,
        Continue,
        Return,
        Begin_shell,
        End_shell,
        Openmp,
        Directive,
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
        append( ([],line) )
      elif type(line) in [ Begin_provider, Cont_provider ]:
        if type(line) == Begin_provider:
          varlist = []
        buffer = map(strip,line.lower.replace(']','').split(','))
        assert len(buffer) > 1
        v = buffer[1]
        varlist.append(v)
        variable_list = find_variables_in_line(line)
        try:
          variable_list.remove(variables[v].same_as)
        except ValueError:
          print v, variables[v].same_as
          raise
        append( (variable_list,line) )
      elif type(line) == End_provider:
        varlist = []
        append( ([],line) )
      elif type(line) == Provide:
        l = line.lower.split()[1:]
        l = filter(lambda x: x not in varlist, l)
        for v in l:
          if v not in variables:
            error.fail(line,"Variable %s is unknown"%(v))
        append( (l,Simple_line(line.i,"!%s"%(line.text),line.filename)) )
      elif type(line) == NoDep:
        l = line.lower.split()[1:]
        for v in l:
          if v not in variables:
            error.fail(line,"Variable %s is unknown"%(v))
        l = map(lambda x: "-%s"%(x), l)
        append( (l,Simple_line(line.i,"!%s"%(line.text),line.filename)) )
      elif type(line) in [ Touch, SoftTouch ]:
        vars = line.lower.split()
        if len(vars) < 2:
          error.fail(line,"Syntax error")
        vars = vars[1:]
        def fun(x):
          main = variables[x].same_as
          return main
        main_vars = make_single( map(fun, vars) )
        check_touch(line,vars,main_vars)
        txt = " ".join(vars)
        append ( (vars,Simple_line(line.i,"!",line.filename)) )
        append ( ([],Simple_line(line.i,"! >>> TOUCH %s"%(txt,),line.filename)) )
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          return [ ([],Simple_line(line.i," call touch_%s"%(x,),line.filename)),
                   ([],Use(line.i," use %s"%(variables[x].fmodule), line.filename)) ]
        result += flatten(map( fun, main_vars ))
        def fun(x):
          if x not in variables:
            error.fail(line,"Variable %s unknown"%(x,))
          return ([],Simple_line(line.i," %s_is_built = .True."%(x,),line.filename))
        result += map( fun, main_vars[:-1] )
        if type(line) == SoftTouch:
          append ( ([],Simple_line(line.i,"! <<< END TOUCH (Soft)",line.filename)) )
        else:
          append ( ([],Provide_all(line.i,"! <<< END TOUCH",line.filename)) )
      elif type(line) == Call:
        l = find_variables_in_line(line)
        l = filter(lambda x: x not in varlist, l)
        sub = find_subroutine_in_line(line)
        if sub not in subroutines:
          t = Simple_line
          append( (l,Simple_line(line.i,line.text,line.filename)) )
        else:
          append( (l,line) )
          if subroutines[sub].touches != []:
            append( ([],Provide_all(line.i,"",line.filename)) )
      elif type(line) == Free:
        vars = line.lower.split()
        vars = vars[1:]
        append( ([],Simple_line(line.i,"!%s"%(line.text),line.filename)) )
        use = map(lambda x: "  use %s"%(variables[x].fmodule),vars)
        for var in vars:
          result += map(lambda x: ([],Use(line.i,x,line.filename)),
            make_single(use))
          result += map(lambda x: ([],Simple_line(line.i,x,line.filename)),
            variables[var].free)
      elif type(line) == Irp_read:
        append( ([],Simple_line(line.i,"!%s"%(line.text),line.filename)) )
      elif type(line) == Irp_write:
        append( ([],Simple_line(line.i,"!%s"%(line.text),line.filename)) )
      elif type(line) in [ Begin_doc, End_doc, Doc ]:
        pass
      else:
        l = find_variables_in_line(line)
        l = filter(lambda x: x not in varlist, l)
        append( (l,line) )
    return result

 #main_result = []
 #for filename,text in preprocessed_text:
 #  main_result.append( (filename, func(filename,text)) )
 #return main_result
  return parallel_loop(func,preprocessed_text)
  
update_variables()
parsed_text = get_parsed_text()


######################################################################

def move_to_top(text,t):
  assert type(text) == list
  assert t in [ NoDep, Declaration, Implicit, Use, Cont_provider ]

  inside = False
  for i in range(len(text)):
    vars, line = text[i]
    if type(line) in [ Begin_provider, Program, Subroutine, Function ]:
      begin = i
      inside = True
    elif type(line) in [ End_provider, End ]:
      inside = False
    elif type(line) == t:
      if inside:
        text.pop(i)
        begin += 1
        text.insert(begin,(vars,line))

  return text

result = []
for filename,text in parsed_text:
  text = move_to_top(text,NoDep)
  text = move_to_top(text,Declaration)
  text = move_to_top(text,Implicit)
  text = move_to_top(text,Use)
  text = move_to_top(text,Cont_provider)
  result.append ( (filename,text) )
parsed_text = result


######################################################################
def build_sub_needs():
  # Needs
  for filename, text in parsed_text:
    sub = None
    in_program = False
    for vars,line in text:
      if type(line) in [ Subroutine, Function ]:
        subname = find_subname(line)
        sub = subroutines[subname]
        sub._needs = []
        sub._to_provide = []
      elif type(line) == End:
        if not in_program:
          sub._needs = make_single(sub._needs)
          sub._to_provide = make_single(sub._to_provide)
          sub = None
      elif type(line) == Program:
        in_program = True
      if sub is not None:
        if type(line) == Declaration:
          sub._to_provide += vars
        sub._needs += vars

build_sub_needs()

#####################################################################

def add_subroutine_needs():
  main_result = []
  for filename, text in parsed_text:
    result = []
    append = result.append
    for vars,line in text:
      if type(line) == Call:
        subname = find_subname(line)
        vars += subroutines[subname].to_provide
      append( (vars,line) )
    main_result.append( (filename, result) )
  return main_result
  
parsed_text = add_subroutine_needs()

######################################################################
def move_variables():

  def func(filename, text):
    result = []
    append = result.append
    # 1st pass
    varlist = []
    ifvars = []
    elsevars = []
    old_varlist = []
    old_ifvars = []
    old_elsevars = []
    revtext = list(text)
    revtext.reverse()
    try:
      for vars,line in revtext:
        if type(line) in [ End_provider,End ]:
          varlist = []
          append( ([],line) )
        elif type(line) in [ Endif, End_select ]:
          old_ifvars.append( list(ifvars) )
          old_elsevars.append( list(elsevars) )
          old_varlist.append( list(varlist) )
          varlist = []
          append( ([],line) )
        elif type(line) == Else:
          elsevars += list(varlist)
          append( (varlist,line) )
          varlist = []
        elif type(line) in [ Elseif, Case ]:
          ifvars += list(varlist)
          append( (varlist,line) )
          if vars != []:
            varlist = old_varlist.pop()
            varlist += vars
            old_varlist.append( list(varlist) )
          varlist = []
        elif type(line) in [ If, Select ]:
          ifvars += list(varlist)
          append( (varlist,line) )
          vars += filter(lambda x: x in elsevars, ifvars)
          ifvars = old_ifvars.pop()
          elsevars = old_elsevars.pop()
          varlist = old_varlist.pop() + vars
        elif type(line) in [ Begin_provider, Program, Subroutine, Function ]:
          varlist += vars
          append( (varlist,line) )
          if old_varlist != [] \
           or old_ifvars != [] \
           or old_elsevars != []:
            error.fail(line,"End if missing")
          varlist = []
        elif type(line) == Provide_all:
          append( (vars,line) )
        else:
          varlist += vars
          append( ([],line) )
    except:
      error.fail(line,"Unable to parse file")

    result.reverse()
  
    # 2nd pass
    text = result
    result = []
    append = result.append
    old_varlist = []
    varlist = []
    try:
      for vars,line in text:
        if vars != []:
          vars = make_single(vars)
        if type(line) in [ Begin_provider, Program, Subroutine, Function ]:
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
          vars += varlist
        elif type(line) in [ End_provider, End ]:
          assert old_varlist == []
          varlist = []
        for v in vars[:]:
          if v[0] == '-':
            vars.remove(v)
            vars.remove(v[1:])
        result.append( (vars,line) )
    except:
      error.fail(line,"Unable to parse file")
    return result

  main_result = []
  for filename,text in parsed_text:
    main_result.append( (filename, func(filename,text)) )
  return main_result
 #return parallel_loop(func,parsed_text)

parsed_text = move_variables()

######################################################################
def build_needs():
  # Needs
  for filename, text in parsed_text:
    var = None
    for vars,line in text:
      if type(line) == Begin_provider:
        buffer = map(strip,line.lower.replace(']',',').split(','))
        var = variables[buffer[1]]
        var.needs = []
        var.to_provide = vars
      elif type(line) == End_provider:
        var.needs = make_single(var.needs)
        var.to_provide = make_single(var.to_provide)
        var = None
      if var is not None:
        var.needs += vars
        if type(line) == Call:
          subname = find_subname(line)
          var.needs += subroutines[subname].needs
        elif type(line) in [ \
          Simple_line,  Assert,
          Do         ,  If,
          Elseif     ,  Select,
        ]: 
          funcs = find_funcs_in_line(line)
          for f in funcs:
            var.needs += subroutines[f].needs 
  for v in variables:
    main = variables[v].same_as 
    if main != v:
      variables[v].needs = variables[main].needs
      variables[v].to_provide = variables[main].to_provide

  # Needed_by
  for v in variables:
    variables[v].needed_by = []
  for v in variables:
    main = variables[v].same_as 
    if main != v:
      variables[v].needed_by = variables[main].needed_by
  for v in variables:
    var = variables[v]
    if var.is_main:
      for x in var.needs:
        variables[x].needed_by.append(var.same_as)
  for v in variables:
    var = variables[v]
    var.needed_by = make_single(var.needed_by)


build_needs()

result = []
for filename,text in parsed_text:
  text = move_to_top(text,NoDep)
  text = move_to_top(text,Declaration)
  text = move_to_top(text,Implicit)
  text = move_to_top(text,Use)
  text = move_to_top(text,Cont_provider)
  result.append ( (filename,text) )
parsed_text = result


######################################################################
from command_line import command_line

def check_opt():
  if not command_line.do_checkopt:
    return

  for filename, text in parsed_text:
    do_level = 0
    for vars,line in text:
     if not type(line) == Provide_all:
      if do_level > 0 and vars != []:
        print "Optimization: %s line %d"%(line.filename,line.i)
        for v in vars:
          print "  PROVIDE ",v
      if type(line) == Do:
        do_level += 1
      elif type(line) == Enddo:
        do_level -= 1
check_opt()

######################################################################
def perform_loop_substitutions():
  main_result = []
  for filename, text in parsed_text:
    result = []
    append = result.append
    for vars,line in text:
      if type(line) in [ Do, If, Elseif ] :
        for k,v in command_line.substituted.items():
          reg = v[1]
          while reg.search(line.text) is not None:
            line.text = re.sub(reg,r'\1%s\3', line.text,count=1)%v[0]
      append( (vars,line) )
    main_result.append( (filename, result) )
  return main_result
  
parsed_text = perform_loop_substitutions()

######################################################################
if __name__ == '__main__':
 for i in range(len(parsed_text)):
  if parsed_text[i][0] == sys.argv[1]:
   print '!-------- %s -----------'%(parsed_text[i][0])
   for line in parsed_text[i][1]:
     print line[1]
     print line[0], line[1].filename
#for i in subroutines:
#  print i, subroutines[i].needs, subroutines[i].to_provide
