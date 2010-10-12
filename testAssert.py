import stat
import os
from sys import executable
import unittest
from subprocess import call, Popen, PIPE
from time import sleep
from socket import socket, error
from errno import EADDRINUSE

TIMEOUT = 5

def socket_status(host, port):
  try:
    socket().bind((host, port),)
    # False if the is free
    return False
  except error, (num, err):
    if num == EADDRINUSE:
      # True if the isn't free
      return True

class BuildoutTestCase(unittest.TestCase):
    """Test all features of buildout profiles"""

    def test_redis(self):
        try:
            call('./bin/redisctl start', shell=True)
            sleep(TIMEOUT)
            self.assertEquals(socket_status('localhost', 6973), True)
        finally:
            call('./bin/redisctl stop', shell=True)

    def test_redis_client(self):
        try:
            call('./bin/redisclientctl start', shell=True)
            sleep(TIMEOUT)
            self.assertEquals(socket_status('localhost', 8888), True)
        finally:
            call('./bin/redisclientctl stop', shell=True)

    def test_sam(self):
        try:
            call('./bin/samctl start', shell=True)
            sleep(TIMEOUT)
            self.assertEquals(socket_status('localhost', 6973), True)
            self.assertEquals(socket_status('localhost', 8888), True)
        finally:
            call('./bin/samctl stop', shell=True)

    def test_lib_txredisapi(self):
        stdout, stderr = Popen('./bin/python -c "import txredisapi"',
                              shell=True,
                              stdout=PIPE,
                              stderr=PIPE).communicate()
        self.assertEquals(stdout, '')
        self.assertEquals(stderr, '')

    def test_lib_twisted(self):
        stdout, stderr = Popen('./bin/python -c "import twisted"',
                              shell=True,
                              stdout=PIPE,
                              stderr=PIPE).communicate()
        self.assertEquals(stdout, '')
        self.assertEquals(stderr, '')
       
    def test_lib_nsisam(self):
        stdout, stderr = Popen('./bin/python -c "import nsisam"',
                              shell=True,
                              stdout=PIPE,
                              stderr=PIPE).communicate()
        self.assertEquals(stdout, '')
        self.assertEquals(stderr, '')

    def test_permissions_file(self):
        filemode = stat.S_IMODE(os.stat('./bin/redisctl').st_mode)
        self.assertEquals(filemode in [448, 493], True)
        filemode = stat.S_IMODE(os.stat('./bin/redisclientctl').st_mode)
        self.assertEquals(filemode in [448, 493], True)
        filemode = stat.S_IMODE(os.stat('./bin/samctl').st_mode)
        self.assertEquals(filemode in [448, 493], True)
        filemode = stat.S_IMODE(os.stat('./bin/redis-server').st_mode)
        self.assertEquals(filemode in [448, 493], True)

    def test_add_user(self):
        add_user_command = [executable,
                          './bin/add-user.py',
                          'test', 'test']

        del_user_command = [executable,
                          './bin/del-user.py',
                          'test']
        try:
            stdout, stderr = Popen(' '.join(add_user_command),
                                  shell=True,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()
            self.assertEquals(stdout, '')
            self.assertEquals(stderr, '')
        finally:
            stdout, stderr = Popen(' '.join(del_user_command),
                                  shell=True,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()
            self.assertEquals(stdout, '')
            self.assertEquals(stderr, '')

if __name__ == "__main__":
    unittest.main()
