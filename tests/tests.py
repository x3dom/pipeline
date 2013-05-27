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


class TaskConfigParserTestCase(unittest.TestCase):


    def setUp(self):
        import ConfigParser
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(os.path.join(PROJECT_ROOT, 'tests/fixtures/bundle_example.ini'))

    def test_config_file(self):

        assert 'task:modelconvert.tasks.convert_model' in self.config.sections()
        assert 'global' in self.config.sections()
        assert 'templates' in self.config.sections()
        assert self.config.get('global', 'name') == 'basic'
        assert self.config.get('global', 'display_name') == 'Basic template'


if __name__ == '__main__':
    unittest.main()
