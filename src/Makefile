PYTHON=python
PYVERSION=$(shell $(PYTHON) -c "import sys; print(sys.version[:3])")
HAS_CYTHON=$(shell which cython &> /dev/null && echo 1 || echo 0)
ifeq ($(HAS_CYTHON),0)

irpf90.exe: 
	cp -f irpf90_python.exe irpf90.exe

else

irpf90.exe: irpf90.so
	gcc build/*/irpf90.o -L/usr/lib64 -lpython$(PYVERSION) -o irpf90.exe

irpf90.so : $(wildcard *.py) irpf90.c
	./cython_setup.py build_ext --inplace

irpf90.c: irpf90.py
	cython --embed irpf90.py

endif

clean:
	rm -f *.c *.so *.pyc *.pyo 2>/dev/null
