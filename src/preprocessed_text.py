#!/usr/bin/python

from irpf90_t import *
from regexps import *
import error

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
  assert not is_doc
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
  if form == Free_form:
    for line in text:
      if line.text[-1] == '&':
        buffer = "%s%s "%(buffer,line.text[:-1].lstrip())
        if number == 0:
          number = line.i
      else:
        if number != 0:
          line.text = "%s%s"%(buffer,line.text.lstrip())
          line.i = number
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
def preprocessed_text(filename):
  file = open(filename,"r")
  lines = file.readlines()
  file.close()
  result = get_text(lines,filename)
  result = execute_shell(result)
  fortran_form = form(result)
  result = remove_comments(result,fortran_form)
  result = remove_continuation(result,fortran_form)
  return result

if __name__ == '__main__': 
  txt = preprocessed_text('testfile.irp.f')
  for line in txt:
    print line
  txt = preprocessed_text('testfile_fixed.irp.f')
  for line in txt:
    print line

