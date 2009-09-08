#!/usr/bin/python

from irpf90_t import *
from util import *
import error
from command_line import command_line

class Variable(object):

  ############################################################
  def __init__(self,text,name = None):
    assert isinstance(text,list)
    assert len(text) > 0
    assert isinstance(text[0],Begin_provider)
    self.text = text
    if name is not None:
      self._name = name.lower()
    self.is_freed   = False
    self.is_read    = False
    self.is_written = False
    self.is_touched = False

  ############################################################
  def name(self):
    '''Name is lowercase'''
    if '_name' not in self.__dict__:
      buffer = None
      for line in self.text:
        if isinstance(line,Begin_provider):
          buffer = line.text.replace(']',',').split(',')
          break
      assert buffer is not None
      if len(buffer) < 3:
        error.fail(line, "Error in Begin_provider line")
      self._name = buffer[1].strip().lower()
    return self._name
  name = property(name)

  ############################################################
  def doc(self):
    if '_doc' not in self.__dict__:
      def f(l): return 
      buffer = filter(lambda l:isinstance(l,Doc), self.text)
      self._doc = map(lambda l: l.text[1:], buffer)
      if buffer == []:
        error.warn(None,"Variable %s is not documented"%(self.name))
    return self._doc
  doc = property(doc)

  ############################################################
  def documented(self):
    if '_documented' not in self.__dict__:
      self._documented = (self.doc != [])
    return self._documented
  documented = property(documented)

  ############################################################
  def others(self):
    if '_others' not in self.__dict__:
      result = []
      f = lambda  l: type(l) in [Begin_provider, Cont_provider]
      lines = filter(f, self.text)
      for line in lines:
        buffer = line.text.replace(']',',').split(',')
        if len(buffer) < 3:
          error.fail(line,"Syntax Error") 
        buffer = buffer[1].strip().lower()
        result.append(buffer)
      result.remove(self.name)
      self._others = result
    return self._others
  others = property(others)

  ############################################################
  def same_as(self):
    if '_same_as' not in self.__dict__:
      if isinstance(self.line,Begin_provider):
        result = self.name
      else:
        buffer = self.text[0].text.replace(']',',').split(',')
        if len(buffer) < 3:
          error.fail(line,"Syntax Error")
        result = buffer[1].strip().lower()
      self._same_as = result
    return self._same_as
  same_as = property(same_as)

  ############################################################
  def allocate(self):
    if '_allocate' not in self.__dict__:
      from variables import variables
      def f(var):
        return variables[var].dim != []
      self._allocate = filter ( f, self.others + [self.name] )
    return self._allocate
  allocate = property(allocate)

  ############################################################
  def dim(self):
    if '_dim' not in self.__dict__:
      line = self.line.text
      buffer = line.replace(']','').split(',',2)
      if len(buffer) == 2:
        self._dim = []
      else:
        buffer = buffer[2].strip()[1:-1].split(',')
        self._dim = map(strip,buffer)
    return self._dim
  dim = property(dim)

  ############################################################
  def type(self):
    if '_type' not in self.__dict__:
      line = self.line.text
      buffer = line.split(',')[0]
      buffer = buffer.split('[')[1].strip()
      if self.dim != '':
        buffer = "%s, allocatable"%(buffer)
      self._type = buffer
    return self._type
  type = property(type)

  ############################################################
  def fmodule(self):
    if '_fmodule' not in self.__dict__:
      self._fmodule = self.line.filename.split('.irp.f')[0]+'_mod'
    return self._fmodule
  fmodule = property(fmodule)

  ############################################################
  def regexp(self):
    if '_regexp' not in self.__dict__:
      import re
      self._regexp = re.compile( \
        r"^.*[^a-z0-9'\"_]+%s([^a-z0-9_]|$)"%(self.name),re.I)
    return self._regexp
  regexp = property(regexp)

  ############################################################
  def line(self):
    if '_line' not in self.__dict__:
      f = lambda l: type(l) in [Begin_provider, Cont_provider]
      lines = filter(f, self.text)
      for line in lines:
        buffer = line.text.replace(']',',').split(',')
        if len(buffer) < 3:
          error.fail(line,"Syntax Error") 
        buffer = buffer[1].strip().lower()
        if self.name == buffer:
          self._line = line
          break
    assert '_line' in self.__dict__
    return self._line
  line = property(line)

  ############################################################
  def header(self):
    if '_header' not in self.__dict__:
      name = self.name
      self._header = [
        "  %s :: %s %s"%(self.type, name, build_dim(self.dim) ),
        "  logical :: %s_is_built = .False."%(name),
      ]
    return self._header
  header = property(header)

  ############################################################
  def toucher(self):
    if '_toucher' not in self.__dict__:
      if self.same_as != self.name:
        self._toucher = ""
      else:
        if '_needed_by' not in self.__dict__:
          import parsed_text
        name = self.name
        result =    [ "subroutine touch_%s"%(name) ,
                      "  use %s"%(self.fmodule),
                      "  implicit none" ]
        if command_line.do_debug:
          length = str(len("touch_%s"%(name)))
          result += [ "  character*(%s), parameter :: irp_here = 'touch_%s'"%(length,name),
                      "  call irp_enter(irp_here)" ]
        result += [   "  %s_is_built = .False."%(name) ] 
        result += map( lambda x: "!DEC$ ATTRIBUTES FORCEINLINE :: touch_%s"%(x), self.needed_by )
        result += map( lambda x: "  call touch_%s"%(x), self.needed_by )
        if command_line.do_debug:
          result.append("  call irp_leave(irp_here)")
        result.append("end subroutine touch_%s"%(name))
        result.append("")
        self._toucher = result
    return self._toucher
  toucher = property(toucher)

  ##########################################################
  def reader(self):
    if '_reader' not in self.__dict__:
      if '_needs' not in self.__dict__:
        import parsed_text
      name = self.name
      result = [ \
      "subroutine reader_%s(irp_num)"%(name),
      "  use %s"%(self.fmodule),
      "  implicit none",
      "  character*(*), intent(in) :: irp_num",
      "  logical                   :: irp_is_open",
      "  integer                   :: irp_iunit" ]
      if command_line.do_debug:
        length = len("reader_%s"%(self.name))
        result += [\
        "  character*(%d), parameter :: irp_here = 'reader_%s'"%(length,name),
        "  call irp_enter(irp_here)" ]
      result += map(lambda x: "  call reader_%s(irp_num)"%(x),self.needs) 
      result += [ \
      "  irp_is_open = .True.",
      "  irp_iunit = 9",
      "  do while (irp_is_open)",
      "   irp_iunit = irp_iunit+1", 
      "   inquire(unit=irp_iunit,opened=irp_is_open)",
      "  enddo",
      "  open(unit=irp_iunit,file='irpf90_%s_'//trim(irp_num),form='FORMATTED',status='OLD',action='READ')"%(name),
      "  read(irp_iunit,*) %s%s"%(name,build_dim(self.dim)),
      "  close(irp_iunit)",
      "  call touch_%s"%(self.same_as),
      "  %s_is_built = .True."%(self.same_as) ]
      if command_line.do_debug:
        result.append("  call irp_leave(irp_here)")
      result.append("end subroutine reader_%s"%(name))
      result.append("")
      self._reader = result
    return self._reader
  reader = property(reader)

  ##########################################################
  def writer(self):
    if '_writer' not in self.__dict__:
      if '_needs' not in self.__dict__:
        import parsed_text
      name = self.name
      result = [ \
      "subroutine writer_%s(irp_num)"%(name),
      "  use %s"%(self.fmodule),
      "  implicit none",
      "  character*(*), intent(in) :: irp_num",
      "  logical                   :: irp_is_open",
      "  integer                   :: irp_iunit" ]
      if command_line.do_debug:
        length = len("writer_%s"%(self.name))
        result += [\
        "  character*(%d), parameter :: irp_here = 'writer_%s'"%(length,name),
        "  call irp_enter(irp_here)" ]
      result += [ \
      "  if (.not.%s_is_built) then"%(self.same_as),
      "    call provide_%s"%(self.same_as),
      "  endif" ]
      result += map(lambda x: "  call writer_%s(irp_num)"%(x),self.needs) 
      result += [ \
      "  irp_is_open = .True.",
      "  irp_iunit = 9",
      "  do while (irp_is_open)",
      "   irp_iunit = irp_iunit+1", 
      "   inquire(unit=irp_iunit,opened=irp_is_open)",
      "  enddo",
      "  open(unit=irp_iunit,file='irpf90_%s_'//trim(irp_num),form='FORMATTED',status='UNKNOWN',action='WRITE')"%(name),
      "  write(irp_iunit,*) %s%s"%(name,build_dim(self.dim)),
      "  close(irp_iunit)" ]
      result += map(lambda x: "  call writer_%s(irp_num)"%(x),self.others) 
      if command_line.do_debug:
        result.append("  call irp_leave(irp_here)")
      result.append("end subroutine writer_%s"%(name))
      result.append("")
      self._writer = result
    return self._writer
  writer = property(writer)

  ##########################################################
  def free(self):
    if '_free' not in self.__dict__:
      name = self.name
      result = [ \
      "subroutine free_%s"%(name),
      "  use %s"%(self.fmodule),
      "  implicit none" ] 
      if command_line.do_debug:
        length = len("free_%s"%(self.name))
        result += [\
        "  character*(%d), parameter :: irp_here = 'free_%s'"%(length,name),
        "  %s_is_built = .False."%(self.same_as) ] 
      if self.dim != []:
        result += [ \
        "  if (allocated(%s)) then"%(name),
        "    deallocate (%s)"%(name),
        "  endif" ]
      if command_line.do_debug:
        result.append("  call irp_leave(irp_here)")
      result.append("end subroutine free_%s"%(name))
      result.append("")
      self._free = result
    return self._free
  free = property(free)

  ##########################################################
  def provider(self):
    if '_provider' not in self.__dict__:
      if '_to_provide' not in self.__dict__:
        import parsed_text
      from variables import variables, build_use, call_provides
      name = self.name
      same_as = self.same_as

      def build_alloc(name):
        self = variables[name]
        if self.dim == []:
           return []

        def do_size():
           result = "     print *, ' size: ("
           result += ','.join(self.dim)
           return result+")'"

        def check_dimensions():
          result = map(lambda x: "(%s>0)"%(dimsize(x)), self.dim)
          result = ".and.".join(result)
          result = "   if (%s) then"%(result)
          return result
 
        def dimensions_OK():
          result = [ "  irp_dimensions_OK = .True." ]
          for i,k in enumerate(self.dim):
              result.append("  irp_dimensions_OK = irp_dimensions_OK.AND.(SIZE(%s,%d)==(%s))"%(name,i+1,dimsize(k)))
          return result

        def do_allocate():
          result = "    allocate(%s(%s),stat=irp_err)"
          result = result%(name,','.join(self.dim))
          return result

        result = [ " if (allocated (%s) ) then"%(name) ]
        result += dimensions_OK()
        result += [\
          "  if (.not.irp_dimensions_OK) then",
          "   deallocate(%s)"%(name) ]
        result.append(check_dimensions())
        result.append(do_allocate())
        result += [\
          "    if (irp_err /= 0) then",
          "     print *, irp_here//': Allocation failed: %s'"%(name),
          do_size(),
          "    endif",
          "   endif",
          "  endif",
          " else" ]
        result.append(check_dimensions())
        result.append(do_allocate())
        result += [\
          "    if (irp_err /= 0) then",
          "     print *, irp_here//': Allocation failed: %s'"%(name),
          do_size(),
          "    endif",
          "   endif",
          " endif" ]
        return result

      result = [ "subroutine provide_%s"%(name) ] 
      result += build_use( [same_as]+self.to_provide )
      result.append("  implicit none")
      length = len("provide_%s"%(name))
      result += [\
      "  character*(%d), parameter :: irp_here = 'provide_%s'"%(length,name),
      "  integer                   :: irp_err ",
      "  logical                   :: irp_dimensions_OK" ] 
      if command_line.do_assert or command_line.do_debug:
        result.append("  call irp_enter(irp_here)")
      result += call_provides(self.to_provide)
      result += flatten( map(build_alloc,[self.same_as]+self.others) )
      result += [\
      "  call bld_%s"%(same_as),
      "  %s_is_built = .True."%(same_as),
      "" ]
      if command_line.do_assert or command_line.do_debug:
        result.append("  call irp_leave(irp_here)")
      result.append("end subroutine provide_%s"%(name) )
      result.append("")
      self._provider = result
    return self._provider
  provider = property(provider)

  ##########################################################
  def builder(self):
    if '_builder' not in self.__dict__:
      if '_needs' not in self.__dict__:
        import parsed_text
      from variables import build_use
      name = self.name
      for line in filter(lambda x: type(x) not in [ Begin_doc, End_doc, Doc], self.text):
        if type(line) == Begin_provider:
          result = [ "subroutine bld_%s"%(name) ]
          result += build_use([name]+self.needs)
        elif type(line) == Cont_provider:
          pass
        elif type(line) == End_provider:
          result.append( "end subroutine bld_%s"%(name) )
          break
        else:
          result.append(line.text)
      self._builder = result
    return self._builder
  builder = property(builder)

######################################################################
if __name__ == '__main__':
  from preprocessed_text import preprocessed_text
  from variables import variables
 #for v in variables.keys():
 #  print v
  for line in variables['grid_eplf_aa'].builder:
    print line
