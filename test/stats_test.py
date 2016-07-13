'''
Created on 13.07.2016

@author: Dominik Lang
'''
import os
import unittest

from stats import Stats


class TestStats(unittest.TestCase):
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files'))
    
    
    def test_Stats(self):
        file_name = 'foo'
        stats = Stats(file_name)  # no exception with an existing file
        self.assertEqual(stats.path, os.path.join(os.getcwd(), file_name))
        
        # non-existing file:
        with self.assertRaises(ValueError):
            stats = Stats('doesnt-exist')
        
        # must be a file not a directory:
        with self.assertRaises(ValueError):
            stats = Stats('a')
    
    
    def test_path(self):
        file_name = 'foo'
        cwd  = os.getcwd()
        stats = Stats(file_name)
        self.assertEqual(cwd, os.getcwd())
        self.assertEqual(stats.path, os.path.abspath('foo'))
        self.assertEqual(stats.path, os.path.join(cwd, 'foo'))
    
    
    def test_modified(self):
        st_mtime = os.stat('foo').st_mtime
        stats = Stats('foo')
        self.assertEqual(stats.modified, st_mtime)
    
    
    def test_size(self):
        st_size = os.stat('foo').st_size
        stats = Stats('foo')
        self.assertEqual(stats.size, st_size)
    
    
    def test___repr__(self):
        stats = Stats('foo')
        fmt = ("<Stats(path='{}',\\n"
               "       modified={}, size={})>")
        expected_repr = fmt.format(stats.path, stats.modified, stats.size)
        self.assertMultiLineEqual(repr(stats), expected_repr)
        stats_hash = stats.hash
        fmt = ("<Stats(path='{}',\\n"
               "       modified={}, size={},\\n"
               "       hash={})>")
        expected_repr = fmt.format(stats.path, stats.modified, stats.size, stats_hash)
        self.assertMultiLineEqual(repr(stats), expected_repr)


if __name__ == "__main__":
    # import sys; sys.argv = ['', 'Test.testStats']
    unittest.main()
