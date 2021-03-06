# file: test_utils.py
# author: mbiokyle29
import logging
import os
import unittest
from shutil import rmtree
from tempfile import mkdtemp, NamedTemporaryFile
from unittest.mock import MagicMock

from place.lib.utils import is_dir, configure_logger


class TestIsDir(unittest.TestCase):
    """ Tests for the is_dir utility function """

    def setUp(self):
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_is_dir_dne(self):
        """ Test that is_dir returns false for a path that doesn't exist """
        non_existant_path = os.path.join(self.test_dir, "foo", "bar", "baz")
        self.assertFalse(is_dir(non_existant_path))

    def test_is_dir_is_file(self):
        """ Test that is_dir returns false for a path that exists but is a file """
        with NamedTemporaryFile(dir=self.test_dir) as temp_file:
            file_path = os.path.join(self.test_dir, temp_file.name)
            self.assertFalse(is_dir(file_path))

    def test_is_dir(self):
        """ Test that is_dir returns true for a path that is a dir """
        with NamedTemporaryFile(dir=self.test_dir) as temp_file:
            file_path = os.path.join(self.test_dir, temp_file.name)
            self.assertFalse(is_dir(file_path))


class TestConfigureLogger(unittest.TestCase):
    """ Tests for the configure_logger utility function """

    def test_configure_logger(self):
        """ Test that configure_logger configured the logger as expected """
        mock_logger = MagicMock()

        configure_logger(mock_logger, logging.INFO)

        mock_logger.setLevel.assert_called_once_with(logging.INFO)
        mock_logger.addHandler.assert_called_once()
