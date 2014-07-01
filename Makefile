PYTHON ?= /usr/bin/env python

all: clean inplace test


clean-bak:
	find . -name "*~" | xargs rm -f

clean-pyc:
	find . -name "*.pyc" | xargs rm -f

clean-so:
	find . -name "*.so" | xargs rm -f
	find . -name "*.pyd" | xargs rm -f

clean-build:
	rm -rf build

clean: clean-build clean-pyc clean-so clean-bak

inplace:
	$(PYTHON) setup.py build_ext -i

nose:
	python make nose

test: clean
	python make test
