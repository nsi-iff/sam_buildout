PYTHON=python
PIP=pip

all: clean sys_deps restfulie redis buildout should_dsl nsisam funkload

clean:
	rm -rf .installed.cfg bin eggs web2py

nsisam:
	pip install https://github.com/nsi-iff/nsi.sam/zipball/master

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
	sudo apt-get install libfile-mimeinfo-perl -y
	sudo update-mime-database /usr/share/mime
	sudo apt-get install unzip -y
	sudo apt-get install python-setuptools -y
	sudo apt-get install python-dev libxml2-dev libxslt1-dev -y
	sudo apt-get install python-webunit python-docutils gnuplot -y

funkload:
	pip install funkload

funkload_deps:
	sudo apt-get install python-dev python-setuptools python-webunit python-docutils gnuplot -y

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

