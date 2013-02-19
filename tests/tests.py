import os
import sys
import unittest
import tempfile

# a little env setup
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)
sys.path.insert(0, PROJECT_ROOT)

from  modelconvert import create_app

class ModelconvertTestCase(unittest.TestCase):

    def setUp(self):
      app = create_app()
      app.config['TESTING'] = True
      self.app = app.test_client()

    def tearDown(self):
        pass

    def test_render_home(self):
        rv = self.app.get('/')
        assert '<!DOCTYPE html>' in rv.data


if __name__ == '__main__':
    unittest.main()
