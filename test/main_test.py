"""
Test the functions of `main.py`.

:author: Dominik Lang
"""
import binascii
from contextlib import redirect_stdout
import io
import os
import unittest
from unittest.mock import create_autospec, PropertyMock

import main
from stats import Stats


class TestMain(unittest.TestCase):
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files'))
    
    
    def test_build_stats(self):
        cwd = os.getcwd()
        
        # non-recursive / general:
        stats, errors = main.build_stats('b')
        files = [stat.path for stat in stats]
        self.assertFalse(errors)
        self.assertEqual(os.getcwd(), cwd)
        
        file_same = os.path.join(cwd, 'b', 'same')
        file_different = os.path.join(cwd, 'b', 'different')
        self.assertIn(file_same, files)
        self.assertIn(file_different, files)
        
        md5_hashes = [binascii.b2a_hex(stat.hash) for stat in stats]
        self.assertIn(b'2145971cf82058b108229a3a2e3bff35', md5_hashes)
        self.assertIn(b'bc70bbb8c964b8b105039a3010775e47', md5_hashes)
        
        # recursive:
        stats, errors = main.build_stats('.', recursive=True)
        self.assertEqual(len(stats), 7)
        self.assertFalse(errors)
        self.assertEqual(os.getcwd(), cwd)
        
        # default to `os.curdir` if no directory specified:
        stats, errors = main.build_stats(None)
        self.assertEqual(len(stats), 2)
        self.assertFalse(errors)
        
        # non-existing directory:
        stats, errors = main.build_stats('does-not-exist')
        self.assertEqual(len(stats), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(os.getcwd(), cwd)
        self.assertEqual(errors[0][0], os.path.join(cwd, 'does-not-exist'))
        self.assertIs(type(errors[0][1]), FileNotFoundError)
    
    
    def test__build_stats(self):
        stats, errors = [], []
        len_stats, len_errors = len(stats), len(errors)
        new_stats, new_errors = main._build_stats(os.getcwd(), ['foo'], stats, errors)
        self.assertIs(stats, new_stats)
        self.assertIs(errors, new_errors)
        self.assertEqual(len(new_stats), len_stats + 1)
        self.assertEqual(len(new_errors), len_errors)
        self.assertEqual(os.path.join(os.getcwd(), 'foo'), new_stats[0].path)
        self.assertEqual(os.lstat('foo').st_size, new_stats[0].size)
        self.assertEqual(os.lstat('foo').st_mtime, new_stats[0].modified)
        self.assertEqual(b'2145971cf82058b108229a3a2e3bff35',
                         binascii.b2a_hex(new_stats[0].hash))
    
    
    def test__build_stats_recursively(self):
        stats, errors = [], []
        len_stats, len_errors = len(stats), len(errors)
        new_stats, new_errors = main._build_stats_recursively(os.getcwd(), stats, errors)
        self.assertIs(stats, new_stats)
        self.assertIs(errors, new_errors)
        self.assertEqual(len(new_stats), len_stats + 7)
        self.assertEqual(len(new_errors), len_errors)
        md5_hashes = [binascii.b2a_hex(stat.hash) for stat in stats]
        self.assertIn(b'2145971cf82058b108229a3a2e3bff35', md5_hashes)
        self.assertIn(b'bc70bbb8c964b8b105039a3010775e47', md5_hashes)
    
    
    def test_identify_duplicates(self):
        self.assertFalse(list(main.identify_duplicates(None)))
        self.assertFalse(list(main.identify_duplicates(main.build_stats('b')[0])))
        
        duplicates_here = main.identify_duplicates(main.build_stats('.')[0])
        self.assertEqual(len(list(duplicates_here)), 1)
        
        # TODO: requires more/better tests
    
    
    def test_process_duplicates(self):
        out = io.StringIO()
        path = 'C:\\foo'
        MockStats = create_autospec(Stats)
        duplicate = MockStats(path)
        type(duplicate).path = PropertyMock(return_value=path)
        print(duplicate.path)
        with redirect_stdout(out):
            main.process_duplicates([duplicate])
        self.assertIn('C:\\foo', out.getvalue())



if __name__ == '__main__':
    unittest.main()
