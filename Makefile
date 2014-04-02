.PHONY: all src man

src:
	$(MAKE) -C $@

man:
	- $(MAKE) -C $@

all: src man

