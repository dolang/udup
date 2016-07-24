"""
Test the `lazy` decorator of `util.py`.

@author: Dominik Lang
"""
import unittest
from util import lazy
from contextlib import redirect_stdout
from io import StringIO


class Test(unittest.TestCase):
    
    def test_lazy(self):
        file_like = StringIO()
        first = SomeClass('first')
        with redirect_stdout(file_like):
            result1 = first.method()
        self.assertEqual('in a method', file_like.getvalue())
        self.assertEqual('leaving method', result1[0])
        file_like = StringIO()
        with redirect_stdout(file_like):
            result1 = first.method()
        # cached value is used, no side effects from print():
        self.assertEqual('', file_like.getvalue())
        self.assertEqual('leaving method', result1[0])

        file_like = StringIO()
        second = SomeClass('second')
        with redirect_stdout(file_like):
            result2 = second.method()
        self.assertEqual('in a method', file_like.getvalue())
        self.assertEqual('leaving method', result2[0])
        file_like = StringIO()
        with redirect_stdout(file_like):
            result2 = second.method()
        # cached value is used, no side effects from print():
        self.assertEqual('', file_like.getvalue())
        self.assertEqual('leaving method', result2[0])
        
        self.assertNotEqual(result1[1], result2[1])
        
        file_like = StringIO()
        with redirect_stdout(file_like):
            result = func()
        self.assertEqual('in a function', file_like.getvalue())
        self.assertEqual('leaving function', result)
        file_like = StringIO()
        with redirect_stdout(file_like):
            result = func()
        # cached value is used, no side effects from print():
        self.assertEqual('', file_like.getvalue())
        self.assertEqual('leaving function', result)



class SomeClass():
    
    def __init__(self, identifier):
        self._id = identifier
    
    @lazy
    def method(self):
        print('in a method', end='', flush=True)
        return 'leaving method', self._id



@lazy
def func():
    print('in a function', end='', flush=True)
    return 'leaving function'



if __name__ == "__main__":
    # import sys; sys.argv = ['', 'Test.test_lazy']
    unittest.main()
