# file: test_config.py
# author: mbiokyle29
import os
import unittest
import logging
from shutil import rmtree
from tempfile import mkdtemp
from unittest.mock import patch

from place.lib.config import PlaceConfig


class TestPlaceConfig(unittest.TestCase):
    """ Tests for the PlaceConfig class """

    def setUp(self):
        self.test_dir = mkdtemp()
        self._old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self._old_cwd)
        rmtree(self.test_dir)

    def test_raw_init(self):
        """ Test a config instance created from raw __init__ call has all defaults """
        instance = PlaceConfig()
        self.assertFalse(instance.debug)
        self.assertFalse(instance.verbose)

    def test_from_kwargs(self):
        """ Test a config instance created via fromKwargs sets the expected values """
        instance = PlaceConfig.fromKwargs(debug=True, verbose=False)
        self.assertTrue(instance.debug)
        self.assertFalse(instance.verbose)
        self.assertEqual(instance.log_level, logging.DEBUG)

    def test_from_kwargs_extras_ignored(self):
        """ Test a config instance created via fromKwargs ignores extra values """
        instance = PlaceConfig.fromKwargs(foo="bar", verbose=True)
        self.assertFalse(instance.debug)
        self.assertTrue(instance.verbose)
        self.assertEqual(instance.log_level, logging.INFO)

    @patch("place.lib.config.configparser.ConfigParser")
    @patch("place.lib.config.path.isfile")
    def test_from_config_file_none_found(self, mocked_isfile, mocked_config_parser):
        """ Test that readConfigFiles returns a default instance when no rc files are found """
        mocked_isfile.return_value = False
        cwd = os.path.abspath(os.path.dirname(__file__))
        instance = PlaceConfig.fromKwargs(
            **PlaceConfig.readConfigFiles(cwd)
        )

        mocked_isfile.assert_called()
        mocked_config_parser.assert_not_called()
        self.assertFalse(instance.debug)
        self.assertFalse(instance.verbose)
        self.assertEqual(instance.log_level, logging.WARN)

    def test_from_config_file_placerc_local(self):
        """ Test that readConfigFiles returns a configured instance when there is .placerc file in cwd """
        with open(".placerc", "w+") as fh:
            fh.write("[place]\n")
            fh.write("verbose = True\n")
            fh.write("debug = True\n")

        instance = PlaceConfig.fromKwargs(
            **PlaceConfig.readConfigFiles(self.test_dir)
        )
        self.assertTrue(instance.debug)
        self.assertTrue(instance.verbose)
        self.assertEqual(instance.log_level, logging.DEBUG)

    def test_from_config_file_placerc_fallback(self):
        """ Test that readConfigFiles returns a configured instance when there is .placerc with no values """
        with open(".placerc", "w+") as fh:
            fh.write("[place]\n")

        instance = PlaceConfig.fromKwargs(
            **PlaceConfig.readConfigFiles(self.test_dir)
        )
        self.assertFalse(instance.debug)
        self.assertFalse(instance.verbose)
        self.assertEqual(instance.log_level, logging.WARN)

    def test_from_config_file_placerc_missing(self):
        """ Test that readConfigFiles handles a malformed .placerc file """
        with open(".placerc", "w+") as fh:
            fh.write("[not_place]\n")

        instance = PlaceConfig.fromKwargs(
            **PlaceConfig.readConfigFiles(self.test_dir)
        )
        self.assertFalse(instance.debug)
        self.assertFalse(instance.verbose)
        self.assertEqual(instance.log_level, logging.WARN)
        self.assertEqual(instance.log_level, logging.WARN)
