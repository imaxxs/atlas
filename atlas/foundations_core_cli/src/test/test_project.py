
import unittest
from mock import patch
from pathlib import Path

from foundations_core_cli.project import Project

class TestProject(unittest.TestCase):

    def setUp(self):
        self._path = None

    def test_name_returns_project_name(self):
        self.assertEqual('superproj', Project('superproj').name())

    def test_name_returns_project_name_different_name(self):
        self.assertEqual('rubber ducky', Project('rubber ducky').name())

    @patch('os.getcwd', lambda: '/path/to/cwd')
    def test_path_returns_relative_path(self):
        self.assertEqual(Path('/path/to/cwd/superproj'), Project('superproj').path())

    @patch('os.getcwd', lambda: '/path/to/cwd')
    def test_path_returns_relative_path_different_project(self):
        self.assertEqual(Path('/path/to/cwd/apples_vs_oranges'), Project('apples_vs_oranges').path())

    @patch('os.getcwd', lambda: '/path/to/different/cwd')
    def test_path_returns_relative_path_different_working_directory(self):
        self.assertEqual(Path('/path/to/different/cwd/superproj'), Project('superproj').path())

    @patch('os.getcwd', lambda: '/path/to/cwd')
    def test_string_path_returns_relative_path(self):
        self.assertEqual('/path/to/cwd/superproj', Project('superproj').string_path())

    @patch('os.getcwd', lambda: '/path/to/cwd')
    def test_string_path_returns_relative_path_different_project(self):
        self.assertEqual('/path/to/cwd/apples_vs_oranges', Project('apples_vs_oranges').string_path())

    @patch('os.getcwd', lambda: '/path/to/different/cwd')
    def test_string_path_returns_relative_path_different_working_directory(self):
        self.assertEqual('/path/to/different/cwd/superproj', Project('superproj').string_path())

    @patch('os.getcwd', lambda: '/path/to/cwd')
    def test_exists_returns_true_on_existing_project(self):
        with self._patch_path_exists('/path/to/cwd/superproj'):
            self.assertTrue(Project('superproj').exists())

    @patch('os.getcwd', lambda: '/path/to/different/cwd')
    def test_exists_returns_false_on_missing_project(self):
        with self._patch_path_exists('/path/to/cwd/superproj'):
            self.assertFalse(Project('superproj').exists())

    @patch('os.getcwd', lambda: '/path/to/cwd')
    def test_exists_returns_true_on_existing_project_different_project(self):
        with self._patch_path_exists('/path/to/cwd/subproj'):
            self.assertTrue(Project('subproj').exists())

    def _patch_path_exists(self, expected_path):
        mock = self._check_dir_callback(expected_path)
        return patch('pathlib.Path.is_dir', mock)

    def _check_dir_callback(self, expected_path):
        def _callback(self):
            return str(self) == expected_path
        return _callback