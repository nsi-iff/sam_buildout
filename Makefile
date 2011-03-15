PYTHON=python

all: clean redis nsisam buildout run_unit_test
clean:
	rm -rf .installed.cfg bin eggs web2py

nsisam:
	@rm -Rf nsi.sam-0.1
	@rm -rf nsi.sam-0.1.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.sam-0.1.tar.gz
	tar -vzxf nsi.sam-0.1.tar.gz
	cd nsi.sam-0.1 && ${PYTHON} setup.py install
	@rm -Rf nsi.sam-0.1
	@rm -rf nsi.sam-0.1.tar.gz

redis:
	@rm -Rf redis-2.0.1
	wget http://redis.googlecode.com/files/redis-2.0.1.tar.gz
	tar zxvf redis-2.0.1.tar.gz
	cd redis-2.0.1 && make
	@rm -f redis-2.0.1.tar.gz

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

run_unit_test:
	$(PYTHON) testAssert.py
	$(PYTHON) tests/testSAM.py

