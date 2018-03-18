# file: test_main.py
# author: mbiokyle29
import os
import unittest
from tempfile import mkdtemp, NamedTemporaryFile

from click.testing import CliRunner

from place.main import cli


class TestMainCli(unittest.TestCase):
    """ Unit tests for the main cli interface """

    def setUp(self):
        self.runner = CliRunner()

    def test_cli_no_target(self):
        """ Test that cli returns a -1 when only a source is given """
        result = self.runner.invoke(cli, ["foo"])
        self.assertEqual(result.exit_code, -1)

    def test_cli_verbose(self):
        """ Test that cli sets the log level to info when given --verbose/-v """
        for verbose_flag in ["--verbose", "-v"]:
            with self.runner.isolated_filesystem() as fs:
                source_file = NamedTemporaryFile(dir=fs, suffix=".txt", delete=False)
                target_name = os.path.join(fs, "foo.txt")
                result = self.runner.invoke(cli, [verbose_flag, source_file.name, target_name])

                self.assertEqual(result.exit_code, 0)

    def test_cli_debug(self):
        """ Test that cli sets the log level to debug when given --debug/-d """
        with self.runner.isolated_filesystem() as fs:
            source_file = NamedTemporaryFile(dir=fs, suffix=".txt", delete=False)
            target_name = os.path.join(fs, "foo.txt")
            result = self.runner.invoke(cli, ["--debug", source_file.name, target_name])

            self.assertEqual(result.exit_code, 0)
            self.assertIn("DEBUG", result.output)

    def test_cli_rename_file(self):
        """ Test that cli renames a file when given 1 source and 1 target (not dir) """
        with self.runner.isolated_filesystem() as fs:
            source_file = NamedTemporaryFile(dir=fs, suffix=".txt", delete=False)
            target_name = os.path.join(fs, "foo.txt")
            result = self.runner.invoke(cli, [source_file.name, target_name])

            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.isfile(target_name))
            self.assertFalse(os.path.isfile(source_file.name))

    def test_cli_rename_dir(self):
        """ Test that cli renames a dir when given 1 source and 1 target (not dir) """
        with self.runner.isolated_filesystem() as fs:
            source_dir = mkdtemp(dir=fs)
            target_name = os.path.join(fs, "foo")
            result = self.runner.invoke(cli, [source_dir, target_name])

            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.isdir(target_name))
            self.assertFalse(os.path.isdir(source_dir))

    def test_cli_move_to_dir_single_file(self):
        """ Test that cli moves a single file to a dir when given 1 source and 1 target dir """
        with self.runner.isolated_filesystem() as fs:
            source_file = NamedTemporaryFile(dir=fs, suffix=".txt", delete=False)
            target_dir = mkdtemp(dir=fs)
            result = self.runner.invoke(cli, [source_file.name, target_dir])

            expected_new_path = os.path.join(target_dir, os.path.basename(source_file.name))
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.isfile(expected_new_path))
            self.assertFalse(os.path.isfile(source_file.name))

    def test_cli_move_to_dir_multiple_files(self):
        """ Test that cli moves multiples files to a dir when given N sources and 1 target dir """
        with self.runner.isolated_filesystem() as fs:
            source_files = [
                NamedTemporaryFile(dir=fs, suffix=".txt", delete=False)
                for i in range(10)
            ]
            target_dir = mkdtemp(dir=fs)

            args = [source_file.name for source_file in source_files]
            args.append(target_dir)
            result = self.runner.invoke(cli, args)

            self.assertEqual(result.exit_code, 0)
            for source_file in source_files:
                expected_new_path = os.path.join(target_dir, os.path.basename(source_file.name))
                self.assertTrue(os.path.isfile(expected_new_path))
                self.assertFalse(os.path.isfile(source_file.name))
