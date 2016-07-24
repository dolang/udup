# -*- coding: utf-8 -*-
"""
File stats.

:author: Dominik Lang
"""

import hashlib
import os

from util import lazy


class Stats(object):
    
    def __init__(self, file_path):
        self._path = os.path.abspath(file_path)
        if not os.path.isfile(self._path):
            raise ValueError("The 'path' must point to an existing file.")
        # else:
        self._hashed = False
        self._stats = os.lstat(self._path)
    
    
    @property
    def path(self):
        return self._path
    
    
    @property
    def modified(self):
        return self._stats.st_mtime
    
    
    @property
    def size(self):
        return self._stats.st_size
    
    
    @property
    @lazy
    def hash(self):
        with open(self.path, 'rb') as file:
            assert os.path.exists(self.path)
            data = file.read()
            hasher = hashlib.md5(data)
            self._hashed = True
            return hasher.digest()
    
    
    def __repr__(self):
        name = self.__class__.__name__
        indent = ' ' * (len(name) + 2)
        hash_part = (',\\n' + indent + 'hash=' + repr(self.hash)) if self._hashed else ''
        fmt = ("<{name}(path='{path}',\\n"
               "{indent}modified={mod}, size={size}"
               "{hash_part})>")
        return fmt.format(name=name, path=self.path, indent=indent, mod=self.modified,
                          size=self.size, hash_part=hash_part)
