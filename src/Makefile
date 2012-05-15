PYTHON=python
PYVERSION=$(shell $(PYTHON) -c "import sys; print(sys.version[:3])")

irpf90.exe: irpf90.so
	gcc build/*/irpf90.o -L/usr/lib64 -lpython$(PYVERSION) -o irpf90.exe

irpf90.so : $(wildcard *.py) irpf90.c
	./cython_setup.py build_ext --inplace

irpf90.c: irpf90.py
	cython --embed irpf90.py

clean:
	rm *.c *.so *.pyc 2>/dev/null
