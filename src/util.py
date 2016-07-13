# -*- coding: utf-8 -*-
"""
Utilities.

:author: Dominik Lang
"""
import functools
import types

class lazy(object):
    """A memoizing decorator for callables with a single result.
    
    When applied on a function or method, the underlying callable is
    run only once when successful, and the result is cached for
    subsequent calls.
    
    This is intentionally simplistic and not supposed to be used on
    callables whose output varies with their arguments or object state.
    
    Thus, callables with parameters aren't supported.  The parameter
    `instance` is reserved for methods and it should not be used to
    decorate functions with a single parameter.
    """

    def __init__(self, decorated_func):
        functools.wraps(decorated_func)(self)
        self._result = None
        self._called = False
    
    
    def __call__(self, instance=None):
        if not self._called:
            instance = (instance,) if instance else ()
            self._result = self.__wrapped__(*instance)
            self._called = True
        return self._result
    
    
    def __get__(self, instance, cls):
        if instance is None:
            return cls
        # else:
        self._instance = instance
        return types.MethodType(self, instance)
