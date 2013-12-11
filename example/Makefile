IRPF90 = python ../src/irpf90.py -I input -a -d
FC     = gfortran
FCFLAGS= -O2

SRC=
OBJ=
LIB=

include irpf90.make

irpf90.make: $(wildcard *.irp.f)
	$(IRPF90)
