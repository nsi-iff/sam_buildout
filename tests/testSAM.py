#encoding: utf-8

import unittest
from should_dsl import should, should_not
from hashlib import sha512
from json import dumps, loads
from subprocess import call
from time import sleep
from restfulie import Restfulie
from os.path import join
from utils import FOLDER_PATH

from datetime import datetime

class SAMTestCase(unittest.TestCase):
    """Test Case to validate all features of SAM"""

    def setUp(self):
        self.uid_list = []
        self.rest = Restfulie.at('http://localhost:8888/').as_('application/json').auth('test','test')
        self.checksum_calculator = sha512()

    def tearDown(self):
        del self.checksum_calculator

    def testSet(self):
        """Test if the data and uid are correctly"""
        dados = {u'value':{u'images':[u'1',u'2', u'3']}}
        response = self.rest.post(value=dados).resource()
        uid = response.key
        checksum = response.checksum

        actual_dict = loads(self.rest.get(key=uid).body)

        today = datetime.today().strftime(u'%d/%m/%y %H:%M')
        from_user = u"test"
        expected_dict = {u"data":dados, u"date":today, u"from_user":from_user}

        self.checksum_calculator.update(dumps(expected_dict))
        expected_checksum = self.checksum_calculator.hexdigest()

        actual_dict |should| equal_to(expected_dict)
        self.rest.get(key='doesnt exist').code |should| equal_to('404')
        self.uid_list.append(uid)

    def testSetWithExpire(self):
        dados = {'test':'ok'}
        response = self.rest.post(value=dados, expire=2).resource()
        uid = response.key
        sleep(3)
        response_code = self.rest.get(key=uid).code
        response_code |should| equal_to('404')

    def testUpdateKeyValue(self):
        """Test if some data is updated correctly"""
        response = self.rest.post(value='SAM TEST 2').resource()
        uid = response.key
        self.uid_list.append(uid)
        checksum = response.checksum

        stored = self.rest.get(key=uid)

        self.checksum_calculator.update(dumps(loads(stored.body)))
        expected_checksum = self.checksum_calculator.hexdigest()

        value = stored.resource()
        value.data |should| equal_to("SAM TEST 2")
        checksum |should| equal_to(expected_checksum)

        self.rest.put(key=uid, value='SAM TEST UPDATE')
        today = datetime.today().strftime('%d/%m/%y %H:%M')
        updated_value = self.rest.get(key=uid).resource()
        data = updated_value.data

        updated_value.history[0].user |should| equal_to('test')
        updated_value.history[0].date |should| equal_to(today)
        data |should| equal_to('SAM TEST UPDATE')

        self.rest.put(key=uid, value='SAM TEST SECOND UPDATE')
        second_updated_value = self.rest.get(key=uid).resource()

        second_updated_value.history[1].user |should| equal_to('test')
        second_updated_value.history[1].date |should| equal_to(today)

    def testDelete(self):
        """Test if some key is deleted correclty"""
        uid = self.rest.post(value='SAM TEST 2').resource().key
        result = self.rest.delete(key=uid).resource()
        result |should| be_deleted
        result = self.rest.delete(key=uid)
        result.code |should| equal_to("404")
        self.uid_list.append(uid)

    def testAuthentication(self):
        """ Test if the server is authenticating correctly """
        sam_with_non_existing_user = Restfulie.at("http://localhost:8888/").as_("application/json").auth('dont', 'exists')
        result = sam_with_non_existing_user.post(value='test')
        self.assertEquals(result.code, "401")

        sam_with_non_existing_user = Restfulie.at("http://localhost:8888/").as_("application/json").auth('test', 'wrongpassword')
        result = sam_with_non_existing_user.post(value='test')
        self.assertEquals(result.code, "401")

    def tearDown(self):
        """Delete all keys"""
        for uid in self.uid_list:
            self.rest.delete(key=uid)

if __name__ == "__main__":
  python_path = join(FOLDER_PATH, "..", 'bin', 'python')
  samctl_path = join(FOLDER_PATH, "..", 'bin', 'samctl')
  adduser_path = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
  deluser_path = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
  try:
    call("%s %s test test" % (python_path, adduser_path), shell=True)
    call("%s start" % samctl_path, shell=True)
    sleep(5)
    unittest.main()
  finally:
    call("%s stop" % samctl_path, shell=True)
    call("%s %s test" % (python_path, deluser_path), shell=True)

