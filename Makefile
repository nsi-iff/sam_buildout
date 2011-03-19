PYTHON=python
PIP=pip

all: clean restfulie redis buildout run_unit_test

clean:
	rm -rf .installed.cfg bin eggs web2py

restfulie:
	@rm -rf restfulie
	git clone git://github.com/caelum/restfulie-py restfulie
	cd restfulie && ${PYTHON} setup.py install
	@rm -rf restfulie

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

