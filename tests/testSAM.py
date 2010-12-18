import unittest
from xmlrpclib import Server
from subprocess import call
from time import sleep
from os.path import join
from utils import FOLDER_PATH

from datetime import datetime

class SAMTestCase(unittest.TestCase):
    """Test Case to validate all features of SAM"""

    def setUp(self):
        self.server = Server("http://test:test@localhost:8888/xmlrpc")
        self.uid_list = []

    def testSet(self):
        """Test if the data and uid are correctly"""
        uid = self.server.set("SAM TEST")
        value = eval(self.server.get(uid))
        today = datetime.today().strftime('%d/%m/%y %H:%M')
        size = 8
        from_user = "test"
        expected_data = "SAM TEST"
        self.assertEqual(value['data'], expected_data)
        self.assertEqual(value['size'], size)
        self.assertEqual(value['from_user'], from_user)
        self.assertEqual(value['date'], today)
        self.assertEqual(self.server.get("doesnt exists"), False)
        self.uid_list.append(uid)

    def testUpdateKeyValue(self):
        """Test if some data is updated correctly"""
        uid = self.server.set("SAM TEST 2")
        data_dict = eval(self.server.get(uid))
        self.assertEquals(data_dict['data'], "SAM TEST 2")
        self.server.update(uid, 'SAM TEST UPDATE')
        data_dict = eval(self.server.get(uid))
        data = data_dict['data']
        self.assertEquals(data, 'SAM TEST UPDATE')
        self.uid_list.append(uid)

    def testDelete(self):
        """Test if some key is deleted correclty"""
        uid = self.server.set("SAM TEST 2")
        result = self.server.delete(uid)
        self.assertEquals(result, True)
        result = self.server.delete(uid)
        self.assertEquals(result, False)
        self.uid_list.append(uid)

    def testAuthentication(self):
        """ Test if the server is authenticating correctly """
        sam_with_non_existing_user = Server("http://nonexisting:userandpass@localhost:8888/xmlrpc")
        result = sam_with_non_existing_user.set('foo')
        self.assertEquals(result, "Authorization Failed!")

        sam_with_wrong_password = Server("http://test:wrongpass@localhost:8888/xmlrpc")
        result = sam_with_wrong_password.get('foo')
        self.assertEquals(result, "Authorization Failed!")

    def tearDown(self):
        """Delete all keys"""
        for uid in self.uid_list:
            self.server.delete(uid)

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

