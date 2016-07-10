udup
====

A simple script to find file duplicates in a directory.


About
-----

First of all, should you use it? The answer is: probably not.  Read
on if you want to know what it's for.

The name *udup* is short for "un-duplicate", and it is named like that
because the term "deduplication" is generally associated with file
systems these days.

It creates MD5-hashes of the files in a directory and identifies
duplicates regardless of their names, whose paths are then printed to
the console.

Right now, it's just a little side project to get my hands dirty on
some APIs and to get started with *GitHub*.  And while it's working
code, I'm sure there a lot of other projects that have solved the same 
problem already, and in a much better way.  Therefore, it's probably
only useful if you're interested in how it works or if want to use
(parts of) the code yourself.

Note: if your goal is to compare two directories with identically-named
files, you may want to have a look at the Python standard library's
``filecmp`` module instead.


Requirements
------------

Python 3.5; it may work with older versions, but that's untested.


Usage
-----

Run the Ant ``build.xml`` to create a *zippapp*, or run ``main.py``
directly.  You probably have to adjust the path to your Python 3.5
executable in ``build.xml`` before running it for the first time.  The
program takes one argument, the directory in which to search for 
duplicates. Windows::

   > python udup.pyz "path\to\directory_with_duplicate_files"
   
     - or -
   
   > python main.py "path\to\directory_with_duplicate_files"
   
Linux::

   $ python3.5 udup.pyz "path/to/directory_with_duplicate_files"
   
     - or -
   
   $ chmod +x main.py
   $ ./main.py "path/to/directory_with_duplicate_files"
   
* Search the directory and its sub-folders recursively with ``-R``.


License
-------

This version is free for any use whatsoever.  You can do anything you
like with the content of the files of this version, without any
obligation, now or in the future.  Ignore the LICENSE and NOTICE files
unless there's a reason for you to be unable to use the content in this
way.  In any case, it comes without any warranties, conditions or
guarantee of fitness for any purpose, either express or implied.

If this is not acceptable or legally permissible in your jurisdiction,
I'm offering it under an Apache v2.0 license as well. In that case, the
terms in the LICENSE file, the NOTICE file and the following notice
apply:

|    Copyright © 2016 Dominik Lang
| 
|    Licensed under the Apache License, Version 2.0 (the "License");
|    you may not use this file except in compliance with the License.
|    You may obtain a copy of the License at
| 
|        http://www.apache.org/licenses/LICENSE-2.0
| 
|    Unless required by applicable law or agreed to in writing, software
|    distributed under the License is distributed on an "AS IS" BASIS,
|    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
|    See the License for the specific language governing permissions and
|    limitations under the License.
