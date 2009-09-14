IRPF90 = irpf90  #-a -d
FC     = gfortran
FCFLAGS= -ffree-line-length-none -O2 

SRC=
OBJ=
LIB=

include irpf90.make

irpf90.make: $(wildcard *.irp.f)
	$(IRPF90)
