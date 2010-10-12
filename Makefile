PYTHON=python

all: clean redisapi redisapisimple nsisam redis buildout run_unit_test
clean:
	rm -rf .installed.cfg bin eggs web2py

redisapi:
	@rm -Rf txredisapi
	git clone git://github.com/fiorix/txredisapi.git
	cd txredisapi && $(PYTHON) setup.py install
	@rm -Rf txredisapi

redisapisimple:
	@rm -Rf redis-2.0.0
	@rm -rf redis-2.0.0.tar.gz
	wget http://github.com/downloads/andymccurdy/redis-py/redis-2.0.0.tar.gz
	tar -vzxf redis-2.0.0.tar.gz
	cd redis-2.0.0 && ${PYTHON} setup.py install
	@rm -Rf redis-2.0.0
	@rm -rf redis-2.0.0.tar.gz

nsisam:
	@rm -Rf nsi.sam-0.1
	@rm -rf nsi.sam-0.1.tar.gz
	wget http://pascal.iff.edu.br/pypi/nsi.sam-0.1.tar.gz
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

