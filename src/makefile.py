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


import os,sys
import irpf90_t
from command_line import command_line
irpdir = irpf90_t.irpdir
mandir = irpf90_t.mandir

FILENAME = "Makefile"

######################################################################
def create():
  has_makefile = True
  try:
    file = open(FILENAME,"r")
  except IOError:
    has_makefile = False
  if has_makefile:
    return
  file = open(FILENAME,"w")
  t = """IRPF90 = irpf90  #-a -d
FC     = gfortran
FCFLAGS= -O2

SRC=
OBJ=
LIB=

include irpf90.make

irpf90.make: $(filter-out %s%%, $(wildcard */*.irp.f)) $(wildcard *.irp.f) $(wildcard *.inc.f) Makefile 
\t$(IRPF90)
"""%(irpdir)
  file.write(t)
  file.close()

######################################################################
def run():
    from modules import modules
    mod = []
    for m in modules.values():
      mod.append(m)

    file = open('irpf90.make','w')
    result = ""
    result += "FC+=-I %s "%(irpdir)
    for i in command_line.include_dir:
       result += "-I %s%s "%(irpdir,i)
    result += "\n"
    result += "SRC += %sirp_stack.irp.F90"%(irpdir)
    result += " %sirp_touches.irp.F90"%(irpdir)
    if command_line.do_openmp:
      result += " %sirp_locks.irp.F90"%(irpdir)
    if command_line.do_profile:
      result += " %sirp_profile.irp.F90"%(irpdir)
    for m in mod:
      result += " %s%s.irp.F90"%(irpdir,m.filename)
      result += " %s%s.irp.module.F90"%(irpdir,m.filename)
    print >>file, result

    result = "OBJ_IRP = "
    for m in mod:
      if not m.is_main:
        result += " %s%s.irp.o"%(irpdir,m.filename)
        result += " %s%s.irp.module.o"%(irpdir,m.filename)
    print >>file, result

    print >>file, "OBJ1 = $(OBJ_IRP) $(OBJ) %sirp_touches.irp.o"%(irpdir),
    if command_line.do_profile:
      print >>file, " %sirp_profile.irp.o"%(irpdir), " irp_rdtsc.o",
    if command_line.do_codelet:
      print >>file, " irp_rdtsc.o",
    if command_line.do_openmp:
      print >>file, " %sirp_locks.irp.o"%(irpdir),
    else:
      print >>file, ""

    all = filter(lambda x: modules[x].is_main, modules)
    all = map(lambda x: x[:-6], all)
    all_o = map(lambda x: "%s.irp.module.o %s.irp.o"%(x,x), all)
    print >>file, "ALL = %s"%(" ".join(all))
    print >>file, "ALL_OBJ = %s"%(" ".join(all_o))
    print >>file, "ALL_OBJ1 = $(patsubst %%, %s%%,$(notdir $(ALL_OBJ)))"%(irpdir)
    print >>file, "all:$(ALL)"
    print >>file, "\t@$(MAKE) -s move"
    print >>file, "ifdef USE_IRPF90_A"
    for m in mod:
      if m.is_main:
        exe = m.filename
        print >>file, "%s: %s%s.irp.o %s%s.irp.module.o irpf90.a"%(exe,irpdir,exe,irpdir,exe)
        print >>file, "\t$(FC) -o $@ %s$@.irp.o %s$@.irp.module.o irpf90.a $(LIB)"%(irpdir,irpdir)
        print >>file, "\t@$(MAKE) -s move"
    print >>file, "else"
    for m in mod:
      if m.is_main:
        exe = m.filename
        print >>file, "%s: %s%s.irp.o %s%s.irp.module.o $(OBJ1)"%(exe,irpdir,exe,irpdir,exe)
        print >>file, "\t$(FC) -o $@ %s$@.irp.o %s$@.irp.module.o $(OBJ1) $(LIB)"%(irpdir,irpdir)
        print >>file, "\t@$(MAKE) -s move"
    print >>file, "endif"

    buffer = ""
    for m in mod:
      filename = "%s%s.irp.o: $(OBJ) %s%s.irp.module.o"%(irpdir,m.filename,irpdir,m.filename)
      needed_modules = filter( lambda x: modules[x].name in m.needed_modules, modules )
      needed_files = map(lambda x: modules[x].filename, needed_modules)
      mds = map (lambda x: " %s%s.irp.module.o"%(irpdir,x),needed_files)
      print >>file, filename," ".join(mds)," ".join(m.includes)
      if not m.is_main:
        buffer += "\t - @echo '"+filename+" ".join(mds)+"' >> %sdist_Makefile\n"%(irpdir)
    print >>file, "%sirp_touches.irp.o:"%(irpdir),
    mds = filter(lambda x: not x.is_main,mod)
    mds = map(lambda x: " %s%s.irp.o %s%s.irp.o"%(irpdir,x.filename,irpdir,x.filename),mds)
    print >>file," ".join(mds)
    if command_line.do_profile:
      print >>file, "%sirp_profile.irp.o:"%(irpdir),
      print >>file," ".join(mds)
    if command_line.do_openmp:
      print >>file, "%sirp_locks.irp.o:"%(irpdir),
      print >>file," ".join(mds)
    

#   print >>file, "%sdist_Makefile:"%(irpdir)
#   print >>file, "\t- @echo FC=$(FC) > %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo FCFLAGS=$(FCFLAGS) >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo LIB=$(LIB) >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo .DEFAULT_GOAL: exe >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo 'exe: $$(EXE).irp.F90 $(OBJ_IRP) $(OBJ) irp_touches.irp.o'  >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo '\t$$(FC) -o $$(EXE) $$(EXE).irp.F90 $(OBJ_IRP) $(OBJ) irp_touches.irp.o $$(LIB)' >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo '%%.o: %%.F90'  >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo '\t$$(FC) $$(FCFLAGS) -c $$*.F90 -o $$*.o' >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo 'clean:' >> %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @echo '\trm *.o *.mod $$(EXE) 2>/dev/null' >> %sdist_Makefile"%(irpdir)
#   print >>file, buffer
#   print >>file, "\t- @echo '\tirp_touches.irp.o: irp_touches.irp.F90 $(OBJ_IRP) $(OBJ) >> %sdist_Makefile"%(irpdir)

#   print >>file, "%%.dist: %sdist_Makefile"%(irpdir)
#   print >>file, "\t- @mkdir -p dist/$*| DO_NOTHING="
#   print >>file, "\t- @cp %s* dist/$*/| DO_NOTHING="%(irpdir)
#   print >>file, "\t- @for i in $(ALL) $(OBJ) irp_touches.irp.o $(ALL_OBJ); do rm dist/$*/$$i ; done| DO_NOTHING="
#   print >>file, "\t- @for i in $(ALL) ; do rm dist/$*/$$i.irp.F90 ; done| DO_NOTHING="
#   print >>file, "\t- @rm dist/$*/{*.irp.f,*.mod,irpf90_entities}| DO_NOTHING="
#   print >>file, "\t- @rm dist/$*/*.mod 2>/dev/null| DO_NOTHING="
#   print >>file, "\t- @echo 'EXE = $*' > dist/$*/Makefile| DO_NOTHING="
#   print >>file, "\t- @cat dist/$*/dist_Makefile >> dist/$*/Makefile| DO_NOTHING="
#   print >>file, "\t- @rm dist/$*/dist_Makefile| DO_NOTHING="
#   print >>file, "\t- @cp %s$*.irp.F90 dist/$*/| DO_NOTHING="%(irpdir)
#   print >>file, "\t- cd dist ; tar -zcvf ../$*.tar.gz $*\n"

    for dir in [ irpdir ] + map(lambda x: irpdir+x, command_line.include_dir):
      print >>file, dir+"%.irp.module.o: "+dir+"%.irp.module.F90"
      print >>file, "\t$(FC) $(FCFLAGS) -c "+dir+"$*.irp.module.F90 -o "+dir+"$*.irp.module.o"
      print >>file, dir+"%.irp.o: "+dir+"%.irp.module.o "+dir+"%.irp.F90"
      print >>file, "\t$(FC) $(FCFLAGS) -c "+dir+"$*.irp.F90 -o "+dir+"$*.irp.o"
      print >>file, dir+"%.irp.o: "+dir+"%.irp.F90"
      print >>file, "\t$(FC) $(FCFLAGS) -c "+dir+"$*.irp.F90 -o "+dir+"$*.irp.o"
      print >>file, dir+"%.o: %.F90"
      print >>file, "\t$(FC) $(FCFLAGS) -c $*.F90 -o "+dir+"$*.o"
      print >>file, dir+"%.o: %.f90\n\t$(FC) $(FCFLAGS) -c $*.f90 -o "+dir+"$*.o"
      print >>file, dir+"%.o: %.f\n\t$(FC) $(FCFLAGS) -c $*.f -o "+dir+"$*.o"
      print >>file, dir+"%.o: %.F\n\t$(FC) $(FCFLAGS) -c $*.F -o "+dir+"$*.o"
      print >>file, dir+"%.irp.F90: irpf90.make\n"
    print >>file, "move:\n\t@mv -f *.mod IRPF90_temp/ 2> /dev/null | DO_NOTHING=\n"
    print >>file, "irpf90.a: $(OBJ) $(OBJ1)\n\t$(AR) crf irpf90.a $(OBJ1)\n"
    print >>file, "clean:\n\trm -rf $(EXE) $(OBJ1) irpf90.a $(ALL_OBJ1) $(ALL)\n"
    print >>file, "veryclean:\n\t- $(MAKE) clean\n"
    print >>file, "\t- rm -rf "+irpdir+" "+mandir+" irpf90.make irpf90_variables dist\n"

    file.close()
