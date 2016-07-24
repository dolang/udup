# -*- coding: utf-8 -*-
"""
Utilities.

:author: Dominik Lang
"""
import functools
import types
import weakref

class lazy(object):
    """A memoizing decorator for callables with a single result.
    
    When applied on a function or method, the underlying callable is
    run only once when successful, and the result is cached for
    subsequent calls.
    
    This is intentionally simplistic and not supposed to be used on
    callables whose output varies with their arguments or object state.
    
    Thus, callables with parameters aren't supported.  The parameter
    `instance` is reserved for methods and should not be used to 
    decorate functions with a single parameter.
    """

    def __init__(self, decorated_func):
        functools.wraps(decorated_func)(self)
        self._called = False
        self._result = None
    
    
    def __call__(self, instance=None):
        return self._on_function() if instance is None else self._on_method(instance)
    
    
    def _on_function(self):
        if not self._called:
            self._result = self.__wrapped__()
            self._called = True
        return self._result
    
    
    def _on_method(self, instance):
        if self._result is None:
            # initialise the decorator to handle instances:
            del self._called
            self._result = weakref.WeakKeyDictionary()
        if not instance in self._result:
            self._result[instance] = self.__wrapped__(instance)
        return self._result[instance]
    
    
    def __get__(self, instance, cls):
        if instance is None:
            return cls
        # else:
        self._instance = instance
        return types.MethodType(self, instance)
