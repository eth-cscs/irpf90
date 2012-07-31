include version
default:
	set -x
	rm *.rpm *.tar.gz *.exe.gz 2> /dev/null ;\
	VERSION=$(VERSION) epm -f portable -a noarch -m noarch irpf90 irpf90.list ;\
	cd noarch ;\
	cp ~/.rpmmacros .;\
	echo "%_topdir $$PWD" > ~/.rpmmacros ;\
	echo "%buildroot %_topdir/buildroot" >> ~/.rpmmacros ;\
	cd ..;\
	VERSION=$(VERSION) epm -a noarch -m noarch -vv -f rpm irpf90 irpf90.list ;\
	cp noarch/.rpmmacros ~;\
	mv noarch/*.tar.gz . ;\
	mv noarch/*.rpm . ;\
	rm -rf noarch;\
	NAME=`basename *.rpm .rpm`;\
	cd ..;\
	git archive --format=tar --prefix=irpf90/ HEAD | gzip > $$OLDPWD/$$NAME-src.tar.gz;\
	cd -;\
	ls $$NAME*;\
	$(HOME)/Python2exe/python2exe.py irpf90 /home/scemama/irpf90/src ;\
	mv irpf90.exe irpf90;\
	gzip irpf90 ;\
	mv irpf90.gz irpf90-$(VERSION)-noarch.exe.gz ;\




version: ../src/version.py
	./make_version.py > version
