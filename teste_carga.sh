#!/bin/bash

set -x
bin/samctl stop
bin/samctl stop
bin/samctl start
bin/add-user.py test test
make load_test
cd tests
fl-run-test testFunkLoad.py
cd ..
make load_test_report
tail -f log/txredis.log

