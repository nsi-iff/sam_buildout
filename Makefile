PYTHON=python

all: clean buildout run_unit_test
clean:
	rm -rf .installed.cfg bin eggs web2py

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

run_unit_test:
	$(PYTHON) testAssert.py
	$(PYTHON) tests/testSAM.py

