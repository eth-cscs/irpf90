#!/usr/bin/python

import irpf90_t
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
FCFLAGS= -ffree-line-length-none -O2

SRC=
OBJ=
LIB=

include irpf90.make

irpf90.make: $(wildcard *.irp.f)
\t$(IRPF90)
"""
  file.write(t)
  file.close()

######################################################################
def run():
  from modules import modules
  mod = []
  for m in modules.keys():
    mod.append(modules[m])

  file = open('irpf90.make','w')

  result = "SRC += %sirp_stack.irp.F90"%(irpdir)
  for m in mod:
    result += " %s%s.irp.F90"%(irpdir,m.name[:-4])
  print >>file, result

  result = "OBJ += %sirp_stack.irp.o"%(irpdir)
  for m in mod:
    if not m.is_main:
      result += " %s%s.irp.o"%(irpdir,m.name[:-4])
  print >>file, result

  print >>file, "OBJ1 = $(patsubst %%, %s%%,$(notdir $(OBJ)))"%(irpdir)

  all = filter(lambda x: modules[x].is_main, modules)
  all = map(lambda x: x[:-6], all)
  all_o = map(lambda x: "%s.irp.o"%(x), all)
  print >>file, "ALL = %s"%(" ".join(all))
  print >>file, "ALL_OBJ = %s"%(" ".join(all_o))
  print >>file, "ALL_OBJ1 = $(patsubst %%, %s%%,$(notdir $(ALL_OBJ)))"%(irpdir)
  print >>file, "all:$(ALL)"
  print >>file, "\t@make -s move"
  for m in mod:
    if m.is_main:
      exe = m.name[:-4]
      print >>file, "%s: %s%s.irp.o $(OBJ1)"%(exe,irpdir,exe)
      print >>file, "\t$(FC) -o $@ %s$@.irp.o $(OBJ1) $(LIB)"%(irpdir)
      print >>file, "\t@make -s move"

  buffer = ""
  for m in mod:
    filename = "%s%s.irp.o:"%(irpdir,m.name[:-4])
    mds = map (lambda x: " %s%s.irp.o"%(irpdir,x[:-4]),m.needed_modules)
    print >>file, filename+" ".join(mds)
    if not m.is_main:
      buffer += "\t - @echo '"+filename+" ".join(mds)+"' >> %sdist_Makefile\n"%(irpdir)

  print >>file, "%sdist_Makefile:"%(irpdir)
  print >>file, "\t- @echo FC=$(FC) > %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo FCFLAGS=$(FCFLAGS) >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo LIB=$(LIB) >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo .DEFAULT_GOAL: exe >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo 'exe: $$(EXE).irp.F90 $(OBJ)'  >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo '\t$$(FC) -o $$(EXE) $$(EXE).irp.F90 $(OBJ) $$(LIB)' >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo '%%.o: %%.F90'  >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo '\t$$(FC) $$(FCFLAGS) -c $$*.F90 -o $$*.o' >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo 'clean:' >> %sdist_Makefile"%(irpdir)
  print >>file, "\t- @echo '\trm *.o *.mod $$(EXE) 2>/dev/null' >> %sdist_Makefile"%(irpdir)
  print >>file, buffer

  print >>file, "%%.dist: %sdist_Makefile"%(irpdir)
  print >>file, "\t- @mkdir -p dist/$*| DO_NOTHING="
  print >>file, "\t- @cp %s* dist/$*/| DO_NOTHING="%(irpdir)
  print >>file, "\t- @for i in $(ALL) $(OBJ) $(ALL_OBJ); do rm dist/$*/$$i ; done| DO_NOTHING="
  print >>file, "\t- @for i in $(ALL) ; do rm dist/$*/$$i.irp.F90 ; done| DO_NOTHING="
  print >>file, "\t- @rm dist/$*/{*.irp.f,*.mod,irpf90_entities}| DO_NOTHING="
  print >>file, "\t- @rm dist/$*/*.mod 2>/dev/null| DO_NOTHING="
  print >>file, "\t- @echo 'EXE = $*' > dist/$*/Makefile| DO_NOTHING="
  print >>file, "\t- @cat dist/$*/dist_Makefile >> dist/$*/Makefile| DO_NOTHING="
  print >>file, "\t- @rm dist/$*/dist_Makefile| DO_NOTHING="
  print >>file, "\t- @cp %s$*.irp.F90 dist/$*/| DO_NOTHING="%(irpdir)
  print >>file, "\t- cd dist ; tar -zcvf ../$*.tar.gz $*\n"

  print >>file, irpdir+"%.irp.o: "+irpdir+"%.irp.F90"
  print >>file, "\t$(FC) $(FCFLAGS) -c "+irpdir+"$*.irp.F90 -o "+irpdir+"$*.irp.o"
  print >>file, irpdir+"%.o: %.F90"
  print >>file, "\t$(FC) $(FCFLAGS) -c $*.F90 -o "+irpdir+"$*.o"
  print >>file, irpdir+"%.o: %.f90\n\t$(FC) $(FCFLAGS) -c $*.f90 -o "+irpdir+"$*.o"
  print >>file, irpdir+"%.o: %.f\n\t$(FC) $(FCFLAGS) -c $*.f -o "+irpdir+"$*.o"
  print >>file, irpdir+"%.o: %.F\n\t$(FC) $(FCFLAGS) -c $*.F -o "+irpdir+"$*.o"
  print >>file, irpdir+"%.irp.F90: irpf90.make\n"
  print >>file, "move:\n\t@mv -f *.mod IRPF90_temp/ 2> /dev/null | DO_NOTHING=\n"
  print >>file, "clean:\n\trm -rf $(EXE) $(OBJ1) $(ALL_OBJ1) $(ALL)\n"
  print >>file, "veryclean:\n\t- make clean\n"
  print >>file, "\t- rm -rf "+irpdir+" "+mandir+" irpf90.make irpf90_variables dist\n"

  file.close()

