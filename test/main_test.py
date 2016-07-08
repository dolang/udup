"""
Test the functions of `main.py`.

:author: Dominik Lang
"""
import binascii
import hashlib
import os
import unittest
import io
from contextlib import redirect_stdout

import main


class TestMain(unittest.TestCase):
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files'))

    
    def test_build_stats(self):
        cwd = os.getcwd()
        stats, errors = main.build_stats('b')
        files = [stat[0] for stat in stats]
        self.assertFalse(errors)
        
        file_same = os.path.join(cwd, 'b', 'same')
        file_different = os.path.join(cwd, 'b', 'different')
        self.assertIn(file_same, files)
        self.assertIn(file_different, files)
        
        file_stats = [stat[1] for stat in stats]
        self.assertTrue(all(type(stat) is tuple for stat in file_stats))
        
        md5_hashes = [binascii.b2a_hex(stat[2]) for stat in stats]
        self.assertIn(b'2145971cf82058b108229a3a2e3bff35', md5_hashes)
        self.assertIn(b'bc70bbb8c964b8b105039a3010775e47', md5_hashes)
    
    
    def test__build_stats(self):
        stats, errors = [], []
        len_stats, len_errors = len(stats), len(errors)
        new_stats, new_errors = main._build_stats(os.getcwd(), ['foo'], stats, errors)
        self.assertIs(stats, new_stats)
        self.assertIs(errors, new_errors)
        self.assertEqual(len(new_stats), len_stats + 1)
        self.assertEqual(len(new_errors), len_errors)
        self.assertEqual(b'2145971cf82058b108229a3a2e3bff35',
                         binascii.b2a_hex(new_stats[0][2]))
    
    
    def test__build_stats_recursively(self):
        stats, errors = [], []
        len_stats, len_errors = len(stats), len(errors)
        new_stats, new_errors = main._build_stats_recursively(os.getcwd(), stats, errors)
        self.assertIs(stats, new_stats)
        self.assertIs(errors, new_errors)
        self.assertEqual(len(new_stats), len_stats + 7)
        self.assertEqual(len(new_errors), len_errors)
        md5_hashes = [binascii.b2a_hex(stat[2]) for stat in stats]
        self.assertIn(b'2145971cf82058b108229a3a2e3bff35', md5_hashes)
        self.assertIn(b'bc70bbb8c964b8b105039a3010775e47', md5_hashes)
    
    
    def test_identify_duplicates(self):
        self.assertFalse(list(main.identify_duplicates(None)))
        self.assertFalse(list(main.identify_duplicates(main.build_stats('b')[0])))
        
        duplicates_here = main.identify_duplicates(main.build_stats('.')[0])
        self.assertEqual(len(list(duplicates_here)), 1)
    
    
    def test_process_duplicates(self):
        out = io.StringIO()
        duplicate = ('C:\\foo', (1, 1.0), b'md5-here')
        with redirect_stdout(out):
            main.process_duplicates([duplicate])
        self.assertIn('C:\\foo', out.getvalue())
    
    
    def test_stat(self):
        stat1 = main._stat('foo')
        self.assertEquals(stat1[0], 5)
        
        raw_stat = os.stat('foo')
        self.assertEqual(stat1, (raw_stat.st_size, raw_stat.st_mtime))
        
        stat2 = main._stat('a\\foo')
        self.assertEqual(stat1[0], stat2[0])
        self.assertNotEqual(stat1, stat2)
        
        stat3 = main._stat('foo')
        self.assertEqual(stat1, stat3)
    
    
    def test_hash(self):
        hash1 = main._hash('foo')
        hash2 = main._hash('a\\foo')
        hasher = hashlib.md5()
        hasher.update(b'foo' + os.linesep.encode('utf-8'))
        hash3 = hasher.digest()
        self.assertEqual(hash1, hash2)
        self.assertEqual(hash2, hash3)



if __name__ == '__main__':
    unittest.main()
