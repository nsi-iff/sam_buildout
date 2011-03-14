import unittest
from xmlrpclib import Server
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
        self.rest = Restfulie.at('http://localhost:8888/').as_('application/json')

    def testSet(self):
        """Test if the data and uid are correctly"""
        uid = self.rest.put({'value':'SAM TEST'}).resource().key
        open('/tmp/log.txt', 'w+').write(uid)
        value = self.rest.get({'key':uid}).resource()
        today = datetime.today().strftime('%d/%m/%y %H:%M')
        size = 8
        from_user = "test"
        expected_data = "SAM TEST"
        self.assertEqual(value.data, expected_data)
        self.assertEqual(value.size, size)
#        self.assertEqual(value.from_user, from_user)
        self.assertEqual(value.date, today)
        self.assertEqual(self.rest.get({'key':'doesnt exist'}).code, '404')
        self.uid_list.append(uid)

    def testUpdateKeyValue(self):
        """Test if some data is updated correctly"""
        uid = self.rest.put({'value':'SAM TEST 2'}).resource().key
        value = self.rest.get({'key':uid}).resource()
        self.assertEquals(value.data, "SAM TEST 2")
        self.rest.post({'key':uid, 'value':'SAM TEST UPDATE'})
        updated_value = self.rest.get({'key':uid}).resource()
        data = updated_value.data
        self.assertEquals(data, 'SAM TEST UPDATE')
        self.uid_list.append(uid)

    def testDelete(self):
        """Test if some key is deleted correclty"""
        uid = self.rest.put({'value':'SAM TEST 2'}).resource().key
        result = self.rest.delete({"key":uid}).resource().deleted
        self.assertEquals(result, True)
        result = self.rest.delete({"key":uid}).resource().deleted
        self.assertEquals(result, False)
        self.uid_list.append(uid)

#    def testAuthentication(self):
#        """ Test if the server is authenticating correctly """
#        sam_with_non_existing_user = Server("http://nonexisting:userandpass@localhost:8888/xmlrpc")
#        result = sam_with_non_existing_user.set('foo')
#        self.assertEquals(result, "Authorization Failed!")

#        sam_with_wrong_password = Server("http://test:wrongpass@localhost:8888/xmlrpc")
#        result = sam_with_wrong_password.get('foo')
#        self.assertEquals(result, "Authorization Failed!")

    def tearDown(self):
        """Delete all keys"""
        for uid in self.uid_list:
            self.rest.delete({'key':uid})

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

