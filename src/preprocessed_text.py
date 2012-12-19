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

from irpf90_t import *
from regexps import *
import error
from command_line import command_line
from util import *

# Local regular expressions
re_endif = re.compile("end\s+if")
re_elseif = re.compile("else\s+if")
re_enddo  = re.compile("end\s+do")
re_endtype= re.compile("end\s+type")
re_endmodule = re.compile("end\s+module")
re_endselect  = re.compile("end\s+select")

# Local variables
Free_form = 0
Fixed_form = 1


######################################################################
# Dictionary of simple statements
simple_dict = {
        "program":               Program         ,
        "subroutine":            Subroutine      ,
        "begin_shell":           Begin_shell     ,
        "end_shell":             End_shell       ,
        "begin_template":        Begin_template  ,
        "end_template":          End_template    ,
        "subst":                 Subst           ,
        "end_doc":               End_doc         ,
        "begin_provider":        Begin_provider  ,
        "&begin_provider":       Cont_provider   ,
        "end_provider":          End_provider    ,
        "assert":                Assert          ,
        "touch":                 Touch           ,
        "soft_touch":            SoftTouch       ,
        "provide":               Provide         ,
        "no_dep":                NoDep           ,
        "free":                  Free            ,
        "irp_if":                Irp_If          ,
        "irp_else":              Irp_Else        ,
        "irp_endif":             Irp_Endif       ,
        "irp_read":              Irp_read        ,
        "irp_write":             Irp_write       ,
        "use":                   Use             ,
        "do":                    Do              ,
        "if":                    If              ,
        "case":                  Case            ,
        "elseif":                Elseif          ,
        "else":                  Else            ,
        "enddo":                 Enddo           ,
        "endif":                 Endif           ,
        "endselect":             End_select      ,
        "end":                   End             ,
        "include":               Include         ,
        "call":                  Call            ,
        "continue":              Continue        ,
        "return":                Return          ,
        "implicit":              Implicit        ,
        "save":                  Declaration     ,
        "function":              Function        ,
        "recursive":             Function        ,
}

def get_type (i, filename, line, is_doc):
  '''Find the type of a text line'''
  assert type(i) == int
  assert type(filename) == str
  assert type(line) == str
  assert type(is_doc) == bool

  line = line.rstrip()
  line = line.replace("$IRP_ALIGN",command_line.align)
  lower_line0 = line.lstrip().lower()
  lower_line = lower_line0.replace("!"," ! ")

  # Replacements
  lower_line = re_elseif.sub("elseif",lower_line)
  lower_line = re_enddo.sub("enddo",lower_line)
  lower_line = re_endtype.sub("endtype",lower_line)
  lower_line = re_endmodule.sub("endmodule",lower_line)
  lower_line = re_endif.sub("endif",lower_line)
  lower_line = re_endselect.sub("endselect",lower_line)

  for c in """()'"[]""":
    lower_line = lower_line.replace(c," "+c+" ")

  buffer = lower_line.split()
  if len(buffer) == 0:
    return [ Empty_line(i,line,filename) ], is_doc

  firstword = buffer[0]
  if firstword.isdigit():
    assert len(buffer) > 1
    buffer = buffer[1:]
    firstword = buffer[0]

  # Identify line
  if firstword == "end_doc":
    return [ End_doc       (i,line,filename) ], False

  if firstword == "begin_doc":
    return [ Begin_doc       (i,line,filename) ], True

  if is_doc:
    return [ Doc (i,line,filename) ], is_doc

  if firstword in simple_dict:
    return [ simple_dict[firstword](i,line,filename) ], is_doc
  
  if firstword in [ "select", "selectcase" ]:
    return [ Select(i,line,filename) ] , is_doc

  if len(lower_line0) > 4:

    if firstword[0] == '#':
      result = [ Simple_line(i,line,filename) ]
      error.warn ( result[0] , 
"""irpf90 may not work with preprocessor directives. You can use
 Irp_if ... Irp_else ... Irp_endif
instead of
 #ifdef ... #else ... #endif""" )
      return result, is_doc

    if firstword.startswith("case("):
     return [ Case(i,line,filename) ], is_doc

    if lower_line0[1:5] == "$omp":
     return [ Openmp(i,line,filename) ], is_doc
    elif lower_line0[1:5] in ["dec$", "dir$"] and command_line.directives:
     return [ Directive(i,line,filename) ], is_doc
    elif lower_line0[1:3] == "$ ":
     return [ Openmp(i,line,filename) ], is_doc

    if re_decl.match(lower_line) is not None:
      if "function" in buffer[1:3]:
        return [ Function (i,line,filename) ], is_doc
      else:
        return [ Declaration (i,line,filename) ], is_doc

    # Detect errors
    if firstword == "dowhile":
      error.fail( Do(i,line,filename) , "'do while' should be in 2 words." )
  
  return [ Simple_line(i,line,filename) ], is_doc


######################################################################
def get_text(lines,filename):
  '''Read the input file and transform it to labeled lines'''
  assert type(filename) == str
  assert type(lines) == list

  result = []
  is_doc = False
  for i,line in enumerate(lines):
    line, is_doc = get_type(i+1,filename,line,is_doc)
    result += line
  return result

######################################################################
def execute_shell(text):
  '''Execute the embedded shell scripts'''
  def fail(l,a,b): error.fail(l,"In Begin_Shell, %s '%s'"%(a,b))
  inside = False
  result = []
  for line in text:
    if inside:
      if type(line) == Begin_shell:
        error.fail(line,"Nested Begin_shell")
      elif type(line) == End_shell:
        inside = False
        # Write script file
        scriptname = "%s%s_shell_%d"%(irpdir,line.filename,line.i)
        file = open(scriptname,'w')
        file.writelines(script)
        file.close()
        scriptname = "%s_shell_%d"%(line.filename,line.i)
        file = open(scriptname,'w')
        file.writelines(script)
        file.close()
        # Execute shell
        import os
        pipe = os.popen("%s < %s"%(shell,scriptname),'r')
        lines = pipe.readlines()
        pipe.close()
        result += get_text(lines,scriptname)
        os.remove(scriptname)
      else:
        script.append(line.text+'\n')
    else:
      if type(line) == Begin_shell:
        inside = True
        begin = line.i
        script = []
        # Find shell executable
        buffer = line.text.split('[')
        if len(buffer) > 2:
          fail(line,"Too many",'[')
        elif len(buffer) < 2:
          fail(line,"Missing",'[')
        buffer = buffer[1]
        buffer = buffer.split(']')
        if len(buffer) > 2:
          fail(line,"Too many",']')
        elif len(buffer) < 2:
          fail(line,"Missing",']')
        shell = buffer[0].strip()
      elif type(line) == End_shell:
        error.fail(line,"Begin_shell missing")
      else:
        result.append(line)
  return result

######################################################################
def execute_templates(text):
  '''Execute the templates'''
  def fail(l,a,b): error.fail(l,"In %s, %s"%(a,b))

  def get_variables(line):
    buffer = line.text.split('[',1)
    if len(buffer)<2:
      fail(line,"Subst","Syntax error")
    buffer = buffer[1].replace(']','')
    buffer = buffer.split(',')
    return map(lambda x: '$%s'%(x.strip()), buffer)

  TEMPLATE = 1
  SUBST = 2
  inside = 0
  result = []
  for line in text:
    if inside == 0:
      if type(line) == Begin_template:
        script = []
        inside = TEMPLATE
        script = "template = \"\"\"\n"
      else:
        result.append(line)
    elif inside == TEMPLATE:
      if type(line) == Begin_template:
        fail(line,"template", "Nested Begin_Template")
      elif type(line) == End_template:
        fail(line,"template","Missing Subst")
      elif type(line) == Subst:
        inside = SUBST
        script += "\"\"\"\n"
        variables = get_variables(line)
        script += "v = []\n"
        subst = ""
      else:
        script += line.text+"\n"
    else: # inside == SUBST
      if type(line) == Begin_template:
        fail(line,"subst","Nested Begin_template")
      elif type(line) == Subst:
        fail(line,"subst","Subst already defined")
      elif type(line) == End_template:
        inside = 0
        subst = subst.rstrip()
        if subst[-2:] == ';;':
          subst = subst[:-2]
        for s in subst.split(';;'):
          buffer = map(lambda x: x.strip(), s.split(';'))
          if len(buffer) != len(variables):
            fail(line,"subst","%d variables defined, and %d substitutions"%(len(variables),len(buffer)))
          script += "v.append( { \\\n"
          for t,v in zip(variables,buffer):
            script += ' "%s": """%s""" ,\n'%(t,v)
          script += "} )\n"
        script += "for d in v:\n  t0 = str(template)\n"
        for v in variables:
          script += "  t0 = t0.replace('%s',d['%s'])\n"%(v,v)
        script += "  print t0\n"
        # Write script file
        scriptname = "%s%s_template_%d"%(irpdir,line.filename,line.i)
        file = open(scriptname,'w')
        file.writelines(script)
        file.close()
        scriptname = "%s_template_%d"%(line.filename,line.i)
        file = open(scriptname,'w')
        file.writelines(script)
        file.close()
        # Execute shell
        import os
        pipe = os.popen("python < %s"%(scriptname),'r')
        lines = pipe.readlines()
        pipe.close()
        result += get_text(lines,scriptname)
        os.remove(scriptname)
      else:
        subst += line.text+'\n'

  return result

######################################################################
def form(text):
  '''Find if the text is in fixed form or in free form'''
  assert type(text) == list
  if len(text) == 0:
    return Free_form
  assert isinstance(text[0],Line)

  re2 = re.compile(r"^\s*[!#]")
  re3 = re.compile(r"^\s*[^ 0-9]+")
  for line in text:
    if type(line) in [ Empty_line, Doc, Openmp, Directive ]:
      pass
    else:
      if len(line.text) > 5:
        test = line.text[0:5]
        if test[0] in "Cc#!*":
          pass
        else:
          if re2.match(test) is None and \
             re3.match(test) is not None:
            return Free_form
          if line.text.rstrip()[-1] == '&':
            return Free_form
  return Fixed_form 

######################################################################
def add_operators(text):
  re_incr = re.compile(r"(\s*)(.*)(\+=)(.*$)",re.S)
  re_decr = re.compile(r"(\s*)(.*)(-=)(.*$)",re.S)
  re_mult = re.compile(r"(\s*)(.*)(\*=)(.*$)",re.S)
  '''Change additional operators'''
  result = []
  for line in text:
    buffer = line.text
    if "+=" in buffer:
      line.text = re.sub(re_incr,r'\1\2=\2+(\4)', buffer)
    elif "-=" in buffer:
      line.text = re.sub(re_decr,r'\1\2=\2-(\4)', buffer)
    elif "*=" in buffer:
      line.text = re.sub(re_mult,r'\1\2=\2*(\4)', buffer)
    result.append(line)
  return result

######################################################################
def remove_comments(text,form):
  '''Remove all comments'''
  result = []

  def remove_after_bang(line):
    match = re_comment.match(line)
    if match is None:
      return line
    else:
      return re_comment.split(line)[1].rstrip()
      
  if form == Free_form:
    for line in text:
      if type(line) in [ Openmp, Doc, Directive] :
         result.append(line)
      elif type(line) == Empty_line:
         pass
      else:
        newline = line.text.lstrip()
        if newline == "" or newline[0] == "!":
          pass
        else:
          line.text = remove_after_bang(line.text)
          result.append(line)
    return result
  else:
    for line in text:
      if type(line) in [ Openmp, Doc, Directive ]:
         result.append(line)
      elif type(line) == Empty_line:
         pass
      else:
        newline = line.text.lstrip()
        if newline == "" or newline[0] == "!":
          pass
        else:
          line.text = remove_after_bang(line.text)
          if line.text[0] in "#123456789 ":
            result.append(line)
    return result

######################################################################
def remove_continuation(text,form):
  '''Removes continuation lines'''
  result = []
  buffer = ""
  number = 0
  t = None
  if form == Free_form:
    for line in text:
      if line.text[-1] == '&':
        buffer = "%s%s\n"%(buffer,line.text)
        if number == 0:
          t = type(line)
          number = line.i
      else:
        if number != 0:
          newline = t(number, \
            "%s%s"%(buffer,line.text), \
            line.filename)
          line = newline
          number = 0
          buffer = ""
        result.append(line)
  else:
    rev_text = list(text)
    rev_text.reverse()
    for line in rev_text:
      is_continuation = False
      if type(line) == Simple_line:
        if len(line.text) >= 6:
          if line.text[5] != ' ':
            is_continuation = True
      if is_continuation:
         buffer = "&\n%s %s %s"%(line.text[:5],line.text[6:],buffer)
      else:
         line.text = line.text+buffer
         result.insert(0,line)
         buffer = ""
  return result

      
######################################################################
def irp_simple_statements(text):
  '''Processes simple statements'''

  def process_irp_rw(line,rw,t):
    assert type(line) == t
    buffer = line.text.split()
    if len(buffer) == 2:
      dummy, variable = buffer
      num = "0"
    elif len(buffer) == 3:
      dummy, variable, num = buffer
    else:
      error.fail(line,"Error in IRP_%s statement"%(rw,))
    variable = variable.lower()
    i = line.i
    f = line.filename
    txt = line.text.lstrip()
    result = [
       Empty_line(i,"!",f),
       t(i,"! >>> %s"%(txt,),variable ),
       Provide_all(i,"   call %ser_%s('%s')"%(rw,variable,num),f),
       Empty_line(i,"! >>> END %s "%(txt,),f ),
       Empty_line(line.i,"!",f),
    ]
    return result
    
  def process_irp_read (line):
    assert type(line) == Irp_read
    return process_irp_rw(line,'read' ,Irp_read )

  def process_irp_write(line):
    assert type(line) == Irp_write
    return process_irp_rw(line,'writ' ,Irp_write)

  def process_return(line):
    assert type(line) == Return
    if command_line.do_assert or command_line.do_debug:
      newline = Simple_line(line.i," call irp_leave(irp_here)",line.filename)
      result = [newline, line]
    else:
      result = [ line ]
    return result

  def debug_conditions(line):
    '''Find condition in assert statement for debug'''
    assert type(line) == Assert
    match = re_test.search(line.text)
    result = []
    if match is not None:
      matches = [ match.group(1).strip(), match.group(3).strip() ]
      for m in matches:
        if not(m.isdigit() or ("'" in m) or (m == "")):
          result.append ( Simple_line (line.i, " print *, '%s = ', %s"%(m,m), line.filename) )
      result.append ( Simple_line (line.i, " print *, ''", line.filename) )
    return result
   
  def process_assert(line):
    assert type(line) == Assert
    if command_line.do_assert:
      condition = "(%s"%(line.text.split('(',1)[1])
      if condition == "":
        error.fail(line,"Error in Assert statement")
      condition_str = condition.replace("'","''")
      i = line.i
      f = line.filename
      txt = line.text.strip()
      result = [
       Empty_line(i, "!", f),
       Empty_line(i, "! >>> %s"%(txt,), f),
       If         (i, "  if (.not.%s) then"%(condition,), f),
       Simple_line(i, "   call irp_trace", f),
       Simple_line(i, "   print *, irp_here//': Assert failed:'", f),
       Simple_line(i, "   print *, ' file: %s, line: %d'"%(f,i), f),
       Simple_line(i, "   print *, '%s'"%(condition_str,), f),
       ] + debug_conditions(line) + [
       Simple_line(i, "   stop 1", f),
       Endif      (i, "  endif", f),
       Empty_line(i, "! <<< END %s"%(txt,), f),
       Empty_line(i, "!", f)
      ]
    else:
      result = []
    return result

  def process_end(line):
    '''Set irp_here variable in provider block'''
    line.text = "end"
    if command_line.do_assert or command_line.do_debug:
      i = line.i
      f = line.filename
      result = [
          Simple_line(i," call irp_leave(irp_here)", f),
          line
        ]
    else:
      result = [ line ]
    return result

  def process_begin_provider(line):
    assert type(line) == Begin_provider
    buffer = line.lower.replace('['," ")
    buffer = buffer.replace(']',"")
    buffer = buffer.split(',')
    if len(buffer) < 2:
      error.fail(line,"Error in Begin_provider statement")
    varname = buffer[1].strip()
    length = len(varname)
    i = line.i
    f = line.filename
    result = [ Begin_provider(i,line.text, (f,varname)),
      Declaration(i,"  character*(%d) :: irp_here = '%s'"%(length,varname), f) ]
    if command_line.do_assert or command_line.do_debug:
      result += [
        Simple_line(i,"  call irp_enter(irp_here)", f),
      ]
    return result

  def process_cont_provider(line):
    assert type(line) == Cont_provider
    buffer = line.lower.replace('['," ")
    buffer = buffer.replace(']',"")
    buffer = buffer.split(',')
    if len(buffer) < 2:
      error.fail(line,"Error in Cont_provider statement")
    varname = buffer[1].strip()
    i = line.i
    f = line.filename
    return [ Cont_provider(i,line.text,(f,varname)) ]

  def process_subroutine(line):
    assert type(line) == Subroutine
    subname = find_subname(line)
    length = len(subname)
    i = line.i
    f = line.filename
    result = [ line,
      Declaration(i,"  character*(%d) :: irp_here = '%s'"%(length,subname), f) ]
    if command_line.do_assert or command_line.do_debug:
      result += [
        Simple_line(i,"  call irp_enter(irp_here)", f),
      ]
    return result

  def process_function(line):
    assert type(line) == Function
    subname = find_subname(line)
    length = len(subname)
    i = line.i
    f = line.filename
    result = [ line,
      Declaration(i,"  character*(%d) :: irp_here = '%s'"%(length,subname), f) ]
    if command_line.do_assert or command_line.do_debug:
      result += [
        Simple_line(i,"  call irp_enter(irp_here)", f),
      ]
    return result


  def process_program(line):
    assert type(line) == Program
    program_name = line.lower.split()[1]
    temp = [ Program(0,"program irp_program",program_name) ] 
    if command_line.do_profile:
      temp += [ Simple_line(0,"call irp_init_timer()",line.filename) ]
    if command_line.do_openmp:
      temp += [ Openmp(0,"!$OMP PARALLEL",line.filename) ]
      temp += [ Openmp(0,"!$OMP MASTER",line.filename) ]
    temp += [ Call(0," call %s"%(program_name),line.filename) ]
    if command_line.do_openmp:
     temp += [ Openmp(0,"!$OMP END MASTER",line.filename) ]
     temp += [ Openmp(0,"!$OMP END PARALLEL",line.filename) ]
    if command_line.do_profile:
      temp += [ Simple_line(0,"call irp_print_timer()",line.filename) ]
    temp += [ Simple_line(0," call irp_finalize_%s()"%(irp_id),line.filename) ]
    temp += [ End(0,"end program",line.filename) ]
    result = temp + \
       process_subroutine( Subroutine(line.i,"subroutine %s"%(program_name,),line.filename) )
    return result

  d = { Irp_read       : process_irp_read,
        Irp_write      : process_irp_write,
        Return         : process_return,
        Assert         : process_assert,
        End            : process_end,
        Begin_provider : process_begin_provider,
        Cont_provider  : process_cont_provider,
        End_provider   : process_end,
        Subroutine     : process_subroutine,
        Function       : process_function,
        Program        : process_program,
      }

  result = []
  for line in text:
    buffer = [ line ]
    for t in d:
      if type(line) == t:
        buffer = d[t](line)
        break
    result += buffer
  return result
    
      
######################################################################
def change_includes(text):
  '''Deals with include files'''
  result = []
  for line in text:
    if type(line) == Include:
     txt = line.text.replace('"',"'").split("'")
     if len(txt) != 3:
       print txt
       error.fail(line,"Error in include statement")
     filename = txt[1].strip()
     try:
       file = open(filename,'r')
       file.close()
       result.append(Include(line.i,"! include '%s'"%filename,filename))
       result += create_preprocessed_text(filename)
     except IOError:
       result.append(Declaration(line.i,line.text,line.filename))
    else:
     result.append(line)
  return result

######################################################################
def process_old_style_do(text):
  '''Changes old-style do loops to new style'''
  assert type(text) == list

  def change_matching_enddo(begin,number):
    for i in range(begin+1,len(text)):
      line = text[i]
      if type(line) in [Continue,Enddo]:
        buffer = line.text.split()
        if buffer[0] == number:
          text[i] = Enddo(line.i,"  enddo",line.filename)
          return
    error.fail(text[begin],"Old-style do loops should end with 'continue' or 'end do'")
      
  result = []
  for i in range(len(text)):
    line = text[i]
    if type(line) == Do:
      buffer = line.text.split()
      try:
       if buffer[1].isdigit():
        number = buffer.pop(1)
        change_matching_enddo(i,number)
        line.text = " ".join(buffer)
      except IndexError:
        pass
    result.append(line)
  return result

######################################################################
def change_single_line_ifs(text):
  '''Changes:
if (test) result 

to

if (test) then
  result
endif'''

  assert type(text) == list
  result = []
  for line in text:
    if type(line) == If:
      if line.lower.endswith("then"):
        result.append(line)
      else:
        buffer = line.text
        begin = buffer.find('(')
        if begin < 0:
          error.fail(line,"Error in if statement")
        level = 0
        instring = False
        for i,c in enumerate(buffer[begin:]):
          if c == "'":
            instring = not instring
          if instring:
            pass
          elif c == '(':
            level +=1
          elif c == ')':
            level -= 1
          if level == 0:
            end = begin+i+1
            break
        if level != 0:
          error.fail(line,"Error in if statement")
        test = buffer[:end]
        code = buffer[end:]
        i = line.i
        f = line.filename
        result.append( If(i,"%s then"%(test,),f) )
        result += get_type(i,f,code,False)[0]
        result.append( Endif(i,"  endif",f) )
    else:
      result.append(line)
  return result

######################################################################
def check_begin_end(text):
  '''Checks x...endx consistence'''

  filter_line = lambda line: type(line) in [ Do, Enddo, If, Endif, \
         Program, Begin_provider, End_provider, \
         Subroutine, Function, End, Begin_doc, End_doc ]
  text = filter(filter_line, text)

  d = { 'do' : Do,         'enddo': Enddo,
        'if' : If,         'endif': Endif,
        '_doc': Begin_doc, 'end_doc': End_doc}
  assert type(text) == list

  def find_matching_end_ifdo(begin,x):
    level = 1
    for i in range(begin+1,len(text)):
      line = text[i]
      if type(line) == d[x]:
        level += 1
      elif type(line) == d["end%s"%(x,)]:
        level -= 1
        if level == 0:
          return True
      elif type(line) in [End, End_provider]:
        break
    error.fail(text[begin],"Missing 'end%s'"%(x,))

  def find_matching_end_subfunpro(begin,x):
    for i in range(begin+1,len(text)):
      line = text[i]
      if type(line) == x:
        return
      if type(line) in [ Subroutine, Function, Program, Begin_provider ]:
        error.fail(text[begin],type(line).str+" is not closed")
    error.fail(text[begin],type(line).str + " is not closed")

  
  level = 0
  for i,line in enumerate(text):
    if type(line) == Begin_doc:
      find_matching_end_ifdo(i,'_doc')
  for i,line in enumerate(text):
    if type(line) == Do:
      find_matching_end_ifdo(i,'do')
    elif type(line) == If:
      find_matching_end_ifdo(i,'if')
    elif type(line) in [Subroutine, Function, Program]:
      level += 1
      find_matching_end_subfunpro(i,End)
    elif type(line) == Begin_provider:
      level += 1
      find_matching_end_subfunpro(i,End_provider)
    elif type(line) == End:
      level -= 1
    elif type(line) == End_provider:
      level -= 1
    if level < 0:
      error.fail(line,"Beginning of block not matched")

  return True

######################################################################
def remove_ifdefs(text):
  assert type(text) == list
  result = []
  do_print = True
  for line in text:
    if type(line) == Irp_If:
      var = line.text.split()[1]
      do_print = var in command_line.defined
    elif type(line) == Irp_Else:
      do_print = not do_print
    elif type(line) == Irp_Endif:
      do_print = True
    else:
      if do_print:
        result.append(line)
  return result

######################################################################
def create_preprocessed_text(filename):
  file = open(filename,"r")
  lines = file.readlines()
  file.close()
  result = get_text(lines,filename)
  result = execute_templates(result)
  result = execute_shell(result)
  fortran_form = form(result)
  result = remove_ifdefs(result)
  result = remove_comments(result,fortran_form)
  result = remove_continuation(result,fortran_form)
  result = add_operators(result)
  result = change_includes(result)
  result = change_single_line_ifs(result)
  result = process_old_style_do(result)
  result = irp_simple_statements(result)
  check_begin_end(result)
  return result

######################################################################
preprocessed_text = parallel_loop( lambda x,y: create_preprocessed_text(x), \
                 map(lambda x: (x,None), irpf90_files ) )

######################################################################
def debug():
  for filename, txt in preprocessed_text:
   if filename == 'invert.irp.f':
    print "=== "+filename+" ==="
    for line in txt:
      print line
  print irpf90_files

if __name__ == '__main__': 
  debug()

