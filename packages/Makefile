include version
default: version
	set -x
	NAME=irpf90-$(VERSION)-noarch-src.tar.gz ;\
	cd ..;\
	git archive --format=tar --prefix=irpf90/ HEAD | gzip > $$OLDPWD/$$NAME;

version: ../src/version.py
	./make_version.py > version
