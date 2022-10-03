import unittest
import os

from .util import ASSETS_PATH


class TestTest(unittest.TestCase):

    def test_asset_path_exists(self):
        self.assertTrue(os.path.exists(ASSETS_PATH))
        self.assertTrue(os.path.isdir(ASSETS_PATH))

    def test_assets_readme_exists(self):
        readme_path = os.path.join(ASSETS_PATH, 'README.rst')
        self.assertTrue(os.path.exists(readme_path))
        self.assertTrue(os.path.isfile(readme_path))
