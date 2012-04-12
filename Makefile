PYTHON=python
PIP=pip

all: clean sys_deps restfulie redis buildout should_dsl nsisam funkload

clean:
	rm -rf .installed.cfg bin eggs web2py

nsisam:
	@rm -Rf nsi.sam-0.2.1
	@rm -rf nsi.sam-0.2.1.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.sam-0.2.1.tar.gz
	tar -vzxf nsi.sam-0.2.1.tar.gz
	cd nsi.sam-0.2.1 && ${PYTHON} setup.py install
	@rm -Rf nsi.sam-0.2.1
	@rm -rf nsi.sam-0.2.1.tar.gz

restfulie:
	${PIP} install restfulie

redis:
	@rm -Rf redis-2.4.8
	wget http://redis.googlecode.com/files/redis-2.4.8.tar.gz
	tar zxvf redis-2.4.8.tar.gz
	cd redis-2.4.8 && make
	@rm -f redis-2.4.8.tar.gz

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

sys_deps:
	sudo apt-get install unzip -y
	sudo apt-get install python-setuptools
	sudo apt-get install python-dev libxml2-dev libxslt1-dev
	sudo apt-get install python-webunit python-docutils gnuplot

funkload:
	pip install funkload

funkload_deps:
	sudo apt-get install python-dev python-setuptools python-webunit python-docutils gnuplot

load_test:
	bin/samctl start
	bin/add-user.py test test
	cd tests && fl-run-bench testFunkLoad.py SamBench.test_sam
	cd tests && fl-build-report --html sam-bench.xml -r funkload_report
	bin/samctl stop
	bin/del-user.py test

load_test_report:
	cd tests && fl-build-report --html sam-bench.xml -r funkload_report

should_dsl:
	${PIP} install should_dsl

test:
	$(PYTHON) testAssert.py
	$(PYTHON) tests/testSAM.py

