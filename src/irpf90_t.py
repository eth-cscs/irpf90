#!/usr/bin/python

irpdir = "IRPF90_temp/"
mandir = "IRPF90_man/"


class Line(object):
  def __init__(self,i,text,filename):
    self.i = i
    self.text = text
    self.filename = filename

class Empty_line(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Empty_line",self.i,self.text)

class Simple_line(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Simple_line",self.i,self.text)

class Declaration(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Declaration",self.i,self.text)

class Continue(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Continue",self.i,self.text)

class Begin_provider(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_provider",self.i,self.text)

class Cont_provider(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Cont_provider",self.i,self.text)

class End_provider(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_provider",self.i,self.text)

class Begin_doc(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_doc",self.i,self.text)

class Doc(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Doc",self.i,self.text)

class End_doc(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_doc",self.i,self.text)

class Begin_shell(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Begin_shell",self.i,self.text)

class End_shell(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_shell",self.i,self.text)

class Assert(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Assert",self.i,self.text)

class Touch(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Touch",self.i,self.text)

class Irp_read(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_read",self.i,self.text)

class Irp_write(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_write",self.i,self.text)

class Irp_If(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_If",self.i,self.text)

class Irp_Else(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_Else",self.i,self.text)

class Irp_Endif(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Irp_Endif",self.i,self.text)

class Openmp(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Openmp",self.i,self.text)

class Use(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Use",self.i,self.text)

class Do(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Do",self.i,self.text)

class Enddo (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Enddo",self.i,self.text)

class If(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("If",self.i,self.text)

class Elseif(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Elseif",self.i,self.text)

class Else(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Else",self.i,self.text)

class Endif(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Endif",self.i,self.text)

class Select(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Select",self.i,self.text)

class Case(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Case",self.i,self.text)

class End_select(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End_select",self.i,self.text)

class Program(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Program",self.i,self.text)

class Subroutine(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Subroutine",self.i,self.text)

class Function(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Function",self.i,self.text)

class Call(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Call",self.i,self.text)

class Provide(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Provide",self.i,self.text)

class Return (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Return",self.i,self.text)

class Include(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Include",self.i,self.text)

class Implicit (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Implicit",self.i,self.text)

class Free(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Free",self.i,self.text)

class End(Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("End",self.i,self.text)

class Provide_all (Line):
  def __init__(self,i,text,filename):
    Line.__init__(self,i,text,filename)
  def __repr__(self):
    return "%20s:%5d : %s"%("Provide_all",self.i,self.text)


######################################################################

def create_irpf90_files():
  result = []
  from command_line import command_line
  import os
  if command_line.do_run:
    def is_irpf90_file(filename):
      return filename.endswith(".irp.f")
    result = filter ( is_irpf90_file, os.listdir(os.getcwd()) )
  return result
irpf90_files = create_irpf90_files()




