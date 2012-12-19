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
from util import *
import error
from command_line import command_line

class Variable(object):

  ############################################################
  def __init__(self,text,label,name = None):
    assert type(text) == list
    assert len(text) > 0
    assert type(text[0]) == Begin_provider
    self.label = label
    self.text = text
    if name is not None:
      self._name = name

  ############################################################
  def is_touched(self):
    if '_is_touched' not in self.__dict__:
      from variables import variables
      result = self.is_read
      for i in self.children:
        if variables[i].is_touched:
          result = True
          break
      self._is_touched = result
    return self._is_touched
  is_touched = property(is_touched)

  ############################################################
  def is_written(self):
    if '_is_written' not in self.__dict__:
      from variables import variables
      result = False
      for i in self.parents:
        if variables[i].is_written:
          result = True
          break
      self._is_written = result
    return self._is_written
  is_written = property(is_written)

  ############################################################
  def is_read(self):
    if '_is_read' not in self.__dict__:
      from variables import variables
      result = False
      for i in self.parents:
        if variables[i].is_read:
          result = True
          break
      self._is_read = result
    return self._is_read
  is_read = property(is_read)

  ############################################################
  def is_main(self):
    if '_is_main' not in self.__dict__:
      self._is_main = (self.name == self.same_as)
    return self._is_main
  is_main = property(is_main)

  ############################################################
  def name(self):
    '''Name is lowercase'''
    if '_name' not in self.__dict__:
      buffer = None
      text = self.text
      for line in text:
        if type(line) == Begin_provider:
          self._name = line.filename[1]
          break
    return self._name
  name = property(name)

  ############################################################
  def doc(self):
    if '_doc' not in self.__dict__:
      text = self.text
      buffer = filter(lambda l:type(l) == Doc, text)
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
  def includes(self):
    if '_includes' not in self.__dict__:
      self._includes = []
      text = self.text
      for line in filter(lambda x: type(x) == Include,text):
        self._includes.append(line.filename)
      make_single(self._includes)
    return self._includes
  includes = property(includes)

  ############################################################
  def others(self):
    if '_others' not in self.__dict__:
      result = []
      append = result.append
      f = lambda  l: type(l) in [Begin_provider, Cont_provider]
      text = self.text
      lines = filter(f, text)
      for line in lines:
        append(line.filename[1])
      result.remove(self.name)
      self._others = result
    return self._others
  others = property(others)

  ############################################################
  def same_as(self):
    if '_same_as' not in self.__dict__:
      if type(self.line) == Begin_provider:
        result = self.name
      else:
        result = self.text[0].filename[1]
      self._same_as = result
    return self._same_as
  same_as = property(same_as)

  ############################################################
  def allocate(self):
    if '_allocate' not in self.__dict__:
      if not self.is_main:
        self._allocate = []
      else:
        from variables import variables
        def f(var):
          return variables[var].dim != []
        self._allocate = filter ( f, self.others + [self.name] )
    return self._allocate
  allocate = property(allocate)

  ############################################################
  def dim(self):
    if '_dim' not in self.__dict__:
      line = self.line.text.split('!')[0]
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
      try:
        buffer = buffer.split('[')[1].strip()
      except IndexError:
        error.fail(None,"Error in definition of %s."%(self.name))
      if self.dim != []:
        buffer = "%s, allocatable"%(buffer)
      self._type = buffer
    return self._type
  type = property(type)

  ############################################################
  def fmodule(self):
    if '_fmodule' not in self.__dict__:
      self._fmodule = self.line.filename[0].split('.irp.f')[0]+'_mod'
    return self._fmodule
  fmodule = property(fmodule)

  ############################################################
  def regexp(self):
    if '_regexp' not in self.__dict__:
      import re
      self._regexp = re.compile( \
        r"([^a-z0-9'\"_]|^)%s([^a-z0-9_]|$)"%(self.name),re.I)
    return self._regexp
  regexp = property(regexp)

  ############################################################
  def line(self):
    if '_line' not in self.__dict__:
      f = lambda l: type(l) in [Begin_provider, Cont_provider]
      text = self.text
      lines = filter(f, text)
      for line in lines:
        buffer = line.filename[1]
        if self._name == buffer:
          self._line = line
          break
    assert '_line' in self.__dict__
    return self._line
  line = property(line)

  ############################################################
  def header(self):
    if '_header' not in self.__dict__:
      name = self.name
      self._header = [ "  %s :: %s %s"%(self.type, name, build_dim_colons(self) ) ]
      if self.dim != [] and command_line.align != '1':
       self._header += ["  !DIR$ ATTRIBUTES ALIGN: %s :: %s"%(command_line.align,name)]
      if self.is_main:
       self._header += [ "  logical :: %s_is_built = .False."%(name) ]
    return self._header
  header = property(header)

  ############################################################
  def toucher(self):
    if '_toucher' not in self.__dict__:
      if not self.is_main:
        self._toucher = []
      else:
        from modules import modules
        from variables import variables
        if '_needed_by' not in self.__dict__:
          import parsed_text
        parents = self.parents
        parents.sort()
        mods = map(lambda x: variables[x].fmodule, parents)
        mods = make_single(mods)+[self.fmodule]
        name = self.name
        result = [ "subroutine touch_%s"%(name) ]
        result += map(lambda x: "  Use %s"%(x),mods)
        result.append("  implicit none")
        if command_line.do_debug:
          length = str(len("touch_%s"%(name)))
          result += [ "  character*(%s) :: irp_here = 'touch_%s'"%(length,name) ]
        if command_line.do_debug:
          result += [ "  call irp_enter(irp_here)" ]
        result += map( lambda x: "  %s_is_built = .False."%(x), parents)
        result.append("  %s_is_built = .True."%(name))
        if command_line.do_debug:
          result.append("  call irp_leave(irp_here)")
        result.append("end subroutine touch_%s"%(name))
        result.append("")
        self._toucher = result
    return self._toucher
  toucher = property(toucher)

  ##########################################################
  def locker(self):
    if '_locker' not in self.__dict__:
      if not command_line.do_openmp:
        self._locker = []
      else:
        from modules import modules
        from variables import variables
        name = self.name
        result  = [ "subroutine irp_lock_%s(set)"%(name) ]
        result += [ "  use omp_lib",
                    "  implicit none",
                    "  logical, intent(in) :: set",
                    "  integer(kind=omp_nest_lock_kind),save :: %s_lock"%(name), 
                    "  integer,save :: ifirst",
                  ]
        if command_line.do_debug:
          length = str(len("irp_lock_%s"%(name)))
          result += [ "  character*(%s) :: irp_here = 'irp_lock_%s'"%(length,name),
                      "  call irp_enter(irp_here)" ]
        result += [ "  if (ifirst == 0) then",
                    "    ifirst = 1",
                    "    call omp_init_nest_lock(%s_lock)"%(name),
                    "  endif",
                    "  if (set) then",
                    "    call omp_set_nest_lock(%s_lock)"%(name),
                    "  else",
                    "    call omp_unset_nest_lock(%s_lock)"%(name),
                    "  endif",
                  ]
        if command_line.do_debug:
          result.append("  call irp_leave(irp_here)")
        result.append("end subroutine irp_lock_%s"%(name))
        result.append("")
        self._locker = result
    return self._locker
  locker = property(locker)

  ##########################################################
  def reader(self):
    if '_reader' not in self.__dict__:
      if not self.is_main:
        self._reader = []
      else:
        if '_needs' not in self.__dict__:
          import parsed_text
        from variables import variables
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
          "  character*(%d) :: irp_here = 'reader_%s'"%(length,name),
          "  call irp_enter(irp_here)" ]
        result += map(lambda x: "  call reader_%s(irp_num)"%(x),self.needs) 
        result += [ \
        "  irp_is_open = .True.",
        "  irp_iunit = 9",
        "  do while (irp_is_open)",
        "   irp_iunit = irp_iunit+1", 
        "   inquire(unit=irp_iunit,opened=irp_is_open)",
        "  enddo"]
        for n in [ name ]+self.others:
          result += [\
          "  open(unit=irp_iunit,file='irpf90_%s_'//trim(irp_num),form='FORMATTED',status='OLD',action='READ')"%(n),
          "  read(irp_iunit,*) %s%s"%(n,build_dim_colons(variables[n])),
          "  close(irp_iunit)" ]
        result += [ \
        "  call touch_%s"%(name),
        "  %s_is_built = .True."%(name) ]
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
      if not self.is_main:
        self._writer = []
      else:
        from variables import variables
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
          "  character*(%d) :: irp_here = 'writer_%s'"%(length,name),
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
        "  enddo" ]
        for n in [ name ] + self.others:
          result += [\
          "  open(unit=irp_iunit,file='irpf90_%s_'//trim(irp_num),form='FORMATTED',status='UNKNOWN',action='WRITE')"%(n),
          "  write(irp_iunit,*) %s%s"%(n,build_dim_colons(variables[n])),
          "  close(irp_iunit)" ]
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
      result = [ "!","! >>> FREE %s"%(self.name),
        "  %s_is_built = .False."%(self.same_as) ] 
      if self.dim != []:
        if command_line.do_memory:
          result += [ \
          "  if (allocated(%s)) then"%(name),
          "    deallocate (%s)"%(name),
          "    print *, 'Deallocating %s'"%(name),
          "  endif" ]
        else:
          result += [ \
          "  if (allocated(%s)) then"%(name),
          "    deallocate (%s)"%(name),
          "  endif" ]
      result.append("! <<< END FREE")
      self._free = result
    return self._free
  free = property(free)

  ##########################################################
  def provider(self):
    if '_provider' not in self.__dict__:
     if not self.is_main:
       self._provider = []
     else:
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
          if command_line.do_memory:
            tmp = "\n   print *, %s, 'Allocating %s(%s)'"
            d = ','.join(self.dim)
            result += tmp%('size('+name+')',name,d)
          return result

        result = [ " if (allocated (%s) ) then"%(name) ]
        result += dimensions_OK()
        result += [\
          "  if (.not.irp_dimensions_OK) then",
          "   deallocate(%s,stat=irp_err)"%(name),
          "   if (irp_err /= 0) then",
          "     print *, irp_here//': Deallocation failed: %s'"%(name),
          do_size(),
          "   endif"]
        if command_line.do_memory:
          result += [\
          "   print *, 'Deallocating %s'"%(name) ]
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

      result = []
      if command_line.directives and command_line.inline in ["all","providers"]:
        result += [ "!DEC$ ATTRIBUTES FORCEINLINE :: provide_%s"%(name) ]
      result += [ "subroutine provide_%s"%(name) ] 
      result += build_use( [same_as]+self.to_provide )
      result.append("  implicit none")
      length = len("provide_%s"%(name))
      result += [\
      "  character*(%d) :: irp_here = 'provide_%s'"%(length,name),
      "  integer                   :: irp_err ",
      "  logical                   :: irp_dimensions_OK" ]
      if command_line.do_openmp:
        result.append(" call irp_lock_%s(.True.)"%(same_as))
      if command_line.do_assert or command_line.do_debug:
        result.append("  call irp_enter(irp_here)")
      result += call_provides(self.to_provide)
      result += flatten( map(build_alloc,[self.same_as]+self.others) )
      result += [ " if (.not.%s_is_built) then"%(same_as),
                  "  call bld_%s"%(same_as),
                  "  %s_is_built = .True."%(same_as), "" ]
      result += [ " endif" ]
      if command_line.do_assert or command_line.do_debug:
        result.append("  call irp_leave(irp_here)")
      if command_line.do_openmp:
        result.append(" call irp_lock_%s(.False.)"%(same_as))
      result.append("end subroutine provide_%s"%(name) )
      result.append("")
      self._provider = result
    return self._provider
  provider = property(provider)

  ##########################################################
  def builder(self):
    if '_builder' not in self.__dict__:
      if not self.is_main:
        self._builder = []
      else:
        import parsed_text
        from variables import build_use, call_provides
        for filename,buffer in parsed_text.parsed_text:
          if self.line.filename[0].startswith(filename):
            break
        text = []
        same_as = self.same_as
        inside = False
        for vars,line in buffer:
          if type(line) == Begin_provider:
            if line.filename[1] == same_as:
              inside = True
            vars = []
          if inside:
            text.append( (vars,line) )
            text += map( lambda x: ([],Simple_line(line.i,x,line.filename)), call_provides(vars) )
            if command_line.do_profile and type(line) == Begin_provider:
              text.append( ( [], Declaration(line.i,"  double precision :: irp_rdtsc, irp_rdtsc1, irp_rdtsc2",line.filename) ) )
              text.append( ( [], Simple_line(line.i,"  irp_rdtsc1 = irp_rdtsc()",line.filename) ) )
          if type(line) == End_provider:
            if inside:
              break
        name = self.name
        text = parsed_text.move_to_top(text,Declaration)
        text = parsed_text.move_to_top(text,Implicit)
        text = parsed_text.move_to_top(text,Use)
        text = map(lambda x: x[1], text)
        for line in filter(lambda x: type(x) not in [ Begin_doc, End_doc, Doc], text):
          if type(line) == Begin_provider:
            result = []
            if command_line.directives and command_line.inline in ["all","builders"]:
              result += [ "!DEC$ ATTRIBUTES INLINE :: bld_%s"%(same_as) ]
            result += [ "subroutine bld_%s"%(name) ]
            result += build_use([name]+self.needs)
          elif type(line) == Cont_provider:
            pass
          elif type(line) == End_provider:
            if command_line.do_profile:
              result += [ "  irp_rdtsc2 = irp_rdtsc()" ,
                          "  call irp_set_timer(%d,(irp_rdtsc2-irp_rdtsc1))"%self.label ]
            result.append( "end subroutine bld_%s"%(name) )
            break
          else:
            result.append(line.text)
        self._builder = result
    return self._builder
  builder = property(builder)

  ##########################################################
  def children(self):
    if '_children' not in self.__dict__:
      if not self.is_main:
        self._children = []
      from variables import variables
      if '_needs' not in self.__dict__:
        import parsed_text
      result = []
      for x in self.needs:
        result.append(x)
        try:
          result += variables[x].children
        except RuntimeError:
          pass # Exception will be checked after
      self._children = make_single(result)
      if self.name in result:
        error.fail(self.line,"Cyclic dependencies:\n%s"%(str(self._children)))
    return self._children
  children = property(children)

  ##########################################################
  def parents(self):
    if '_parents' not in self.__dict__:
      if not self.is_main:
        self._parents = []
      else:
        from variables import variables
        if '_needed_by' not in self.__dict__:
          import parsed_text
        result = []
        for x in self.needed_by:
          result.append(x)
          try:
            result += variables[x].parents
          except RuntimeError:
            pass # Exception will be checked after
        self._parents = make_single(result)
        if self.name in result:
          error.fail(self.line,"Cyclic dependencies:\n%s"%(str(self._parents)))
    return self._parents
  parents = property(parents)

######################################################################
if __name__ == '__main__':
  from preprocessed_text import preprocessed_text
  from variables import variables
 #for v in variables.keys():
 #  print v
  for line in variables['e_loc'].parents:
    print line
