import unittest
from os.path import dirname, abspath, join
from json import dumps, loads
from base64 import b64encode
from restfulie import Restfulie
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data

FOLDER_PATH = abspath(dirname(__file__))

class SamBench(FunkLoadTestCase):
    """This test use a configuration file Simple.conf."""

    def __init__(self, *args, **kwargs):
        FunkLoadTestCase.__init__(self, *args, **kwargs)
        """Setting up the benchmark cycle."""
        self.server_url = self.conf_get('main', 'url')
        self.sam = Restfulie.at('http://localhost:8888/').auth('test', 'test').as_('application/json')
        self.uid_list = []
        size_multiplier = int(self.conf_get('main', 'request_size'))
        self.data = b64encode('a' * 40 * 1024 * size_multiplier)

    def test_sam(self):
        server_url = self.server_url
        self.setBasicAuth('test', 'test')

        # The description should be set in the configuration file

        body = dumps({'value': self.data})

        # begin of test ---------------------------------------------
        self.put(server_url, description='Send many requests with 5mb each.',
                  params=Data('application/json', body))
        response = loads(self.getBody())
        self.uid = response['key']
        # end of test -----------------------------------------------

    def tearDown(self):
        self.sam.delete(key=self.uid)


if __name__ in  ('__main__', 'main'):
       unittest.main()
