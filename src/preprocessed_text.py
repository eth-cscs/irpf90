#!/usr/bin/python

from irpf90_t import *
from regexps import *
import error
from command_line import command_line

# Local regular expressions
re_endif = re.compile("end\s+if")
re_elseif = re.compile("else\s+if")
re_enddo  = re.compile("end\s+do")
re_endselect  = re.compile("end\s+select")

# Local variables
Free_form = 0
Fixed_form = 1


######################################################################
def get_type (i, filename, line, is_doc):
  '''Find the type of a text line'''
  assert isinstance(i,int)
  assert isinstance(filename,str)
  assert isinstance(line,str)
  assert isinstance(is_doc,bool)

  line = line.rstrip()
  lower_line0 = line.lstrip().lower()
  lower_line  = lower_line0.replace("!"," ! ")

  # Replacements
  lower_line = re_elseif.sub("elseif",lower_line)
  lower_line = re_enddo.sub("enddo",lower_line)
  lower_line = re_endif.sub("endif",lower_line)
  lower_line = re_endselect.sub("endselect",lower_line)
  for c in """()'"[]""":
    lower_line = lower_line.replace(c," ")

  buffer = lower_line.split()
  if len(buffer) == 0:
    return [ Empty_line(i,line,filename) ], is_doc

  firstword = buffer[0]
  if firstword.isdigit():
    assert len(buffer) > 1
    buffer = buffer[1:]
    firstword = buffer[0]

  # Detect errors
  if firstword == "dowhile":
    error.fail( Do(i,line,filename) , "'do while' should be in 2 words." )
  
  # Identify line
  if firstword == "end_doc":
    return [ End_doc       (i,line,filename) ], False

  if firstword == "begin_doc":
    return [ Begin_doc       (i,line,filename) ], True

  if is_doc:
    return [ Doc (i,line,filename) ], is_doc

  # Dictionary of simple statements
  simple_dict = {
        "program":              [ Program         (i,line,filename) ] ,
        "subroutine":           [ Subroutine      (i,line,filename) ] ,
        "begin_shell":          [ Begin_shell     (i,line,filename) ] ,
        "end_shell":            [ End_shell       (i,line,filename) ] ,
        "end_doc":              [ End_doc         (i,line,filename) ] ,
        "begin_provider":       [ Begin_provider  (i,line,filename) ] ,
        "&begin_provider":      [ Cont_provider   (i,line,filename) ] ,
        "end_provider":         [ End_provider    (i,line,filename) ] ,
        "assert":               [ Assert          (i,line,filename) ] ,
        "touch":                [ Touch           (i,line,filename) ] ,
        "provide":              [ Provide         (i,line,filename) ] ,
        "free":                 [ Free            (i,line,filename) ] ,
        "irp_if":               [ Irp_If          (i,line,filename) ] ,
        "irp_else":             [ Irp_Else        (i,line,filename) ] ,
        "irp_endif":            [ Irp_Endif       (i,line,filename) ] ,
        "irp_read":             [ Irp_read        (i,line,filename) ] ,
        "irp_write":            [ Irp_write       (i,line,filename) ] ,
        "use":                  [ Use             (i,line,filename) ] ,
        "do":                   [ Do              (i,line,filename) ] ,
        "selectcase":           [ Select          (i,"",filename) ,
                                  Simple_line     (i,line,filename) ] ,
        "select":               [ Select          (i,"",filename) ,
                                  Simple_line     (i,line,filename) ] ,
        "if":                   [ If              (i,line,filename) ] ,
        "case":                 [ Case            (i,line,filename) ] ,
        "elseif":               [ Elseif          (i,line,filename) ] ,
        "else":                 [ Else            (i,line,filename) ] ,
        "enddo":                [ Enddo           (i,line,filename) ] ,
        "endif":                [ Endif           (i,line,filename) ] ,
        "endselect":            [ End_select      (i,line,filename) ] ,
        "end":                  [ End             (i,line,filename) ]  ,
        "include":              [ Include         (i,line,filename) ] ,
        "call":                 [ Call            (i,line,filename) ]  ,
        "continue":             [ Continue        (i,line,filename) ] ,
        "return":               [ Return          (i,line,filename) ] ,
        "implicit":             [ Implicit        (i,line,filename) ] ,
        "save":                 [ Declaration     (i,line,filename) ] ,
        "function":             [ Function        (i,line,filename) ] ,
        "recursive":            [ Function        (i,line,filename) ] ,
  }

  if firstword in simple_dict.keys():
    return simple_dict[firstword], is_doc
  
  if len(lower_line0) > 4:

    if firstword[0] == '#':
      result = [ Simple_line(i,line,filename) ]
      error.warn ( result , 
"""irpf90 may not work with preprocessor directives. You can use
 Irp_if ... Irp_else ... Irp_endif
instead of
 #ifdef ... #else ... #endif""" )
      return result, is_doc

    if firstword.startswith("case("):
     return [ Case(i,line,filename) ], is_doc

    if lower_line0[1:5] == "$omp":
     return [ Openmp(i,line,filename) ], is_doc

    if re_decl.match(lower_line) is not None:
      if "function" in buffer[1:3]:
        return [ Function (i,line,filename) ], is_doc
      else:
        return [ Declaration (i,line,filename) ], is_doc

  return [ Simple_line(i,line,filename) ], is_doc


######################################################################
def get_text(lines,filename):
  '''Read the input file and transform it to labeled lines'''
  assert isinstance(filename,str)
  assert isinstance(lines,list)

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
      if isinstance(line,Begin_shell):
        error.fail(line,"Nested Begin_shell")
      elif isinstance(line,End_shell):
        inside = False
        # Write script file
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
      else:
        script.append(line.text+'\n')
    else:
      if isinstance(line,Begin_shell):
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
      elif isinstance(line,End_shell):
        error.fail(line,"Begin_shell missing")
      else:
        result.append(line)
  return result

######################################################################
def form(text):
  '''Find if the text is in fixed form or in free form'''
  assert isinstance(text,list)
  if len(text) == 0:
    return Free_form
  assert isinstance(text[0],Line)

  re2 = re.compile(r"^\s*[!#]")
  re3 = re.compile(r"^\s*[^ 0-9]+")
  for line in text:
    if isinstance(line,Empty_line) or \
       isinstance(line,Doc)        or \
       isinstance(line,Openmp):
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
      if isinstance(line,Openmp) or \
         isinstance(line,Doc):
         result.append(line)
      elif isinstance(line,Empty_line):
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
      if isinstance(line,Openmp) or \
         isinstance(line,Doc):
         result.append(line)
      elif isinstance(line,Empty_line):
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
        buffer = "%s%s "%(buffer,line.text[:-1].lstrip())
        if number == 0:
          t = type(line)
          number = line.i
      else:
        if number != 0:
          newline = t(number, \
            "%s%s"%(buffer,line.text.lstrip()), \
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
      if isinstance(line,Simple_line):
        if len(line.text) >= 6:
          if line.text[5] != ' ':
            is_continuation = True
      if is_continuation:
         buffer = "%s %s"%(line.text[6:].lstrip(),buffer)
      else:
         line.text = line.text+buffer
         result.insert(0,line)
         buffer = ""
  return result

      
######################################################################
def irp_simple_statements(text):
  '''Processes simple statements'''

  def process_irp_rw(line,rw,t):
    assert isinstance(line,t)
    buffer = line.text.split()
    if len(buffer) == 2:
      dummy, variable = buffer
      num = "0"
    elif len(buffer) == 3:
      dummy, variable, num = buffer
    else:
      error.fail(line,"Error in IRP_%s statement"%(rw,))
    i = line.i
    f = line.filename
    txt = line.text.lstrip()
    result = [
       Simple_line(i,"!",f),
       Simple_line(i,"! >>> %s"%(txt,),f ),
       Provide_all(i,"   call %ser_%s('%s')"%(rw,variable,num),f),
       Simple_line(i,"! >>> END %s "%(txt,),f ),
       Simple_line(line.i,"!",f),
    ]
    return result
    
  def process_irp_read (line):
    assert isinstance(line,Irp_read)
    return process_irp_rw(line,'read' ,Irp_read )

  def process_irp_write(line):
    assert isinstance(line,Irp_write)
    return process_irp_rw(line,'writ' ,Irp_write)

  def process_return(line):
    assert isinstance(line,Return)
    if command_line.do_assert or command_line.do_debug:
      newline = Simple_line(line.i," call irp_leave(irp_here)",line.filename)
      result = [newline, line]
    else:
      result = [ line ]
    return result

  def debug_conditions(line):
    '''Find condition in assert statement for debug'''
    assert isinstance(line,Assert)
    match = re_test.search(line.text)
    if match is None:
      result = [ line ]
    else:
      result = []
      matches = [ match.group(1).strip(), match.group(3).strip() ]
      for m in matches:
        if not(m.isdigit() or ("'" in m) or (m == "")):
          result.append ( Simple_line (line.i, " print *, '%s = ', %s"%(m,m), line.filename) )
      result.append ( Simple_line (line.i, " print *, ''", line.filename) )
    return result
   
  def process_assert(line):
    assert isinstance(line,Assert)
    if command_line.do_assert:
      condition = line.text.split(None,1)[1]
      if condition == "":
        error.fail(line,"Error in Assert statement")
      condition_str = condition.replace("'","''")
      i = line.i
      f = line.filename
      txt = line.text.strip()
      result = [
       Simple_line(i, "!", f),
       Simple_line(i, "! >>> %s"%(txt,), f),
       If         (i, "  if (.not.%s) then"%(condition,), f),
       Simple_line(i, "   call irp_trace", f),
       Simple_line(i, "   print *, irp_here//': Assert failed:'", f),
       Simple_line(i, "   print *, ' file: %s, line: %d'"%(f,i), f),
       Simple_line(i, "   print *, '%s'"%(condition_str,), f),
       ] + debug_conditions(line) + [
       Simple_line(i, "   stop 1", f),
       Endif      (i, "  endif", f),
       Simple_line(i, "! <<< END %s"%(txt,), f),
       Simple_line(i, "!", f)
      ]
    else:
      result = []
    return result

  def process_end(line):
    '''Set irp_here variable in provider block'''
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
    assert isinstance(line,Begin_provider)
    buffer = line.text.replace('['," ")
    buffer = buffer.replace(']',"")
    buffer = buffer.split(',')
    if len(buffer) < 2:
      error.fail(line,"Error in Begin_provider statement")
    varname = buffer[1].strip().lower()
    length = len(varname)
    i = line.i
    f = line.filename
    result = [ line,
      Declaration(i,"  character*(%d), parameter :: irp_here = '%s'"%(length,varname), f) ]
    if command_line.do_assert or command_line.do_debug:
      result += [
        Simple_line(i,"  call irp_enter(irp_here)", f),
      ]
    return result

  def process_subroutine(line):
    assert isinstance(line,Subroutine)
    buffer = line.text.split('(')
    if len(buffer) > 1:
      buffer = " ".join(buffer[:-1])
    else:
      buffer = buffer[0]
    buffer = buffer.lower().split()
    if len(buffer) != 2:
      print buffer
      error.fail(line,"Error in Subroutine statement")
    subname = buffer[1]
    length = len(subname)
    i = line.i
    f = line.filename
    result = [ line,
      Declaration(i,"  character*(%d), parameter :: irp_here = '%s'"%(length,subname), f) ]
    if command_line.do_assert or command_line.do_debug:
      result += [
        Simple_line(i,"  call irp_enter(irp_here)", f),
      ]
    return result

  def process_function(line):
    assert isinstance(line,Function)
    buffer = line.text.split('(')
    if (len(buffer) < 2):
      error.fail(line,"Error in Function statement")
    buffer = " ".join(buffer[:-1])
    buffer = buffer.lower().split()
    if len(buffer) < 2:
      error.fail(line,"Error in Function statement")
    subname = buffer[-1]
    length = len(subname)
    i = line.i
    f = line.filename
    result = [ line,
      Declaration(i,"  character*(%d), parameter :: irp_here = '%s'"%(length,subname), f) ]
    if command_line.do_assert or command_line.do_debug:
      result += [
        Simple_line(i,"  call irp_enter(irp_here)", f),
      ]
    return result


  def process_program(line):
    assert isinstance(line,Program)
    program_name = line.text.split()[1].lower()
    result = [ Program(0,"",program_name) ] + \
       process_subroutine( Subroutine(line.i,"subroutine %s"%(program_name,),line.filename) )
    return result

  d = { Irp_read       : process_irp_read,
        Irp_write      : process_irp_write,
        Return         : process_return,
        Assert         : process_assert,
        End            : process_end,
        Begin_provider : process_begin_provider,
        End_provider   : process_end,
        Subroutine     : process_subroutine,
        Function       : process_function,
        Program        : process_program,
      }

  result = []
  for line in text:
    buffer = [ line ]
    for t in d.keys():
      if isinstance(line,t):
        buffer = d[t](line)
        break
    result += buffer
  return result
    
      
######################################################################
def change_includes(text):
  '''Deals with include files'''
  result = []
  for line in text:
    if (isinstance(line,Include)):
     txt = line.text.replace('"',"'").split("'")
     if len(txt) != 3:
       print txt
       error.fail(line,"Error in include statement")
     filename = txt[1].strip()
     try:
       file = open(filename,'r')
       file.close()
       result += create_preprocessed_text(filename)
      #result += get_text(file.readlines(), filename)
     except IOError:
       result.append(line)
    else:
     result.append(line)
  return result

######################################################################
def process_old_style_do(text):
  '''Changes old-style do loops to new style'''
  assert isinstance(text,list)

  def change_matching_enddo(begin,number):
    for i in range(begin+1,len(text)):
      line = text[i]
      if isinstance(line,Continue) or \
         isinstance(line,Enddo):
        buffer = line.text.split()
        if buffer[0] == number:
          text[i] = Enddo(line.i,"  enddo",line.filename)
          return
    error.fail(text[begin],"Old-style do loops should end with 'continue' or 'end do'")
      
  result = []
  for i in range(len(text)):
    line = text[i]
    if isinstance(line,Do):
      buffer = line.text.split()
      if buffer[1].isdigit():
        number = buffer.pop(1)
        change_matching_enddo(i,number)
        line.text = " ".join(buffer)
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

  assert isinstance(text,list)
  result = []
  for line in text:
    if isinstance(line,If):
      if line.text.endswith("then"):
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

  def filter_line(line):
    for type in [ Do, Enddo, If, Endif, Begin_provider, End_provider, \
                  Subroutine, Function, End, Begin_doc, End_doc ]:
      if isinstance(line,type):
        return True
    return False

  text = filter(filter_line, text)

  d = { 'do' : Do,         'enddo': Enddo,
        'if' : If,         'endif': Endif,
        '_doc': Begin_doc, 'end_doc': End_doc}
  assert isinstance(text,list)

  def find_matching_end_ifdo(begin,x):
    level = 1
    for i in range(begin+1,len(text)):
      line = text[i]
      if isinstance(line,d[x]):
        level += 1
      elif isinstance(line,d["end%s"%(x,)]):
        level -= 1
        if level == 0:
          return True
      elif isinstance(line,End) or \
           isinstance(line,End_provider):
        break
    error.fail(text[begin],"Missing 'end%s'"%(x,))

  def find_matching_end_subfunpro(begin,x):
    for i in range(begin+1,len(text)):
      line = text[i]
      if isinstance(line,x):
        return
      for t in [ Subroutine, Function, Begin_provider ]:
        if isinstance(line,t):
          error.fail(text[begin],"Subroutine/Function/Provider is not closed")
    error.fail(text[begin],"Subroutine/Function/Provider is not closed")

  
  level = 0
  for i,line in enumerate(text):
    if isinstance(line,Begin_doc):
      find_matching_end_ifdo(i,'_doc')
  for i,line in enumerate(text):
    if isinstance(line,Do):
      find_matching_end_ifdo(i,'do')
    elif isinstance(line,If):
      find_matching_end_ifdo(i,'if')
    elif isinstance(line,Subroutine):
      level += 1
      find_matching_end_subfunpro(i,End)
    elif isinstance(line,Function):
      level += 1
      find_matching_end_subfunpro(i,End)
    elif isinstance(line,Begin_provider):
      level += 1
      find_matching_end_subfunpro(i,End_provider)
    elif isinstance(line,End):
      level -= 1
    elif isinstance(line,End_provider):
      level -= 1
    if level < 0:
      error.fail(line,"Beginning of block not matched")

  return True

######################################################################
def remove_ifdefs(text):
  assert isinstance(text,list)
  result = []
  do_print = True
  for line in text:
    if isinstance(line,Irp_If):
      var = line.text.split()[1]
      do_print = var in command_line.defined
    elif isinstance(line,Irp_Else):
      do_print = not do_print
    elif isinstance(line,Irp_Endif):
      do_print = True
    else:
      if do_print:
        result.append(line)
  return result

######################################################################
def move_to_top(text,t):
  assert isinstance(text,list)
  assert t in [ Declaration, Implicit, Use ]

  begin = -1
  for i in range(len(text)):
    line = text[i]
    if isinstance(line,Begin_provider) or \
       isinstance(line,Subroutine)     or \
       isinstance(line,Function):
      begin = i
    elif isinstance(line,t):
      text.pop(i)
      begin += 1
      text.insert(begin,line)

  return text

######################################################################
def create_preprocessed_text(filename):
  file = open(filename,"r")
  lines = file.readlines()
  file.close()
  result = get_text(lines,filename)
  result = execute_shell(result)
  fortran_form = form(result)
  result = remove_ifdefs(result)
  result = remove_comments(result,fortran_form)
  result = remove_continuation(result,fortran_form)
  result = change_includes(result)
  result = change_single_line_ifs(result)
  result = process_old_style_do(result)
  result = irp_simple_statements(result)
  result = move_to_top(result,Declaration)
  result = move_to_top(result,Implicit)
  result = move_to_top(result,Use)
  return result

######################################################################
preprocessed_text = []
for filename in irpf90_files:
   result = create_preprocessed_text(filename)
   check_begin_end(result)
   preprocessed_text.append( (filename, result) )

######################################################################
def debug():
  for filename, txt in preprocessed_text:
    print "=== "+filename+" ==="
    for line in txt:
      print line
  print irpf90_files

if __name__ == '__main__': 
  debug()

