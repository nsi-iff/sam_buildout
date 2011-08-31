PYTHON=python
PIP=pip

all: clean sys_deps unzip restfulie redis buildout should_dsl nsisam test

unzip:
	sudo apt-get install unzip -y

clean:
	rm -rf .installed.cfg bin eggs web2py

pip_install:
	sudo apt-get install python-setuptools
	sudo easy_install pip

nsisam:
	@rm -Rf nsi.sam-0.1
	@rm -rf nsi.sam-0.1.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.sam-0.1.tar.gz
	tar -vzxf nsi.sam-0.1.tar.gz
	cd nsi.sam-0.1 && ${PYTHON} setup.py install
	@rm -Rf nsi.sam-0.1
	@rm -rf nsi.sam-0.1.tar.gz

restfulie:
	${PIP} install restfulie

redis:
	@rm -Rf redis-2.0.1
	wget http://redis.googlecode.com/files/redis-2.0.1.tar.gz
	tar zxvf redis-2.0.1.tar.gz
	cd redis-2.0.1 && make
	@rm -f redis-2.0.1.tar.gz

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

sys_deps:
	sudo apt-get install python-setuptools python-dev libxml2-dev libxslt1-dev python-profiler

should_dsl:
	${PIP} install should_dsl

test:
	$(PYTHON) testAssert.py
	$(PYTHON) tests/testSAM.py

