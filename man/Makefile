RST2MAN=rst2man -d -t

default: man1/irpman.1.gz man1/irpf90.1.gz

options.rst: ../src/command_line.py
	python ../src/command_line.py > options.rst

man1/irpf90.1.gz: irpf90.rst options.rst
	rm -f $@ ; $(RST2MAN) --title="IRP Fortran 90" irpf90.rst man1/irpf90.1 ; gzip man1/irpf90.1

man1/irpman.1.gz: irpman.rst
	rm -f $@ ; $(RST2MAN) --title="IRP man" irpman.rst man1/irpman.1 ; gzip man1/irpman.1
