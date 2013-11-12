.PHONY: all src man

all: src man

src:
	$(MAKE) -C $@

man:
	- $(MAKE) -C $@

