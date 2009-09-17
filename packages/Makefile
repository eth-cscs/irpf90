include version
default:
	rm *.rpm *.tar.gz 2> /dev/null ;\
	VERSION=$(VERSION) epm -m noarch irpf90 irpf90.list ;\
	cd noarch ;\
	cp ~/.rpmmacros .;\
	echo "%_topdir $$PWD" > ~/.rpmmacros ;\
	echo "%buildroot %_topdir/buildroot" >> ~/.rpmmacros ;\
	cd ..;\
	VERSION=$(VERSION) epm -m noarch -vv -f rpm irpf90 irpf90.list ;\
	cp noarch/.rpmmacros ~;\
	mv noarch/*.tar.gz . ;\
	mv noarch/*.rpm . ;\
	rm -rf noarch

version: ../src/version.py
	./make_version.py > version
