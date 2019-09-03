python-dlinfo
=============

Python wrapper for libc's dlinfo

Install
-------

.. code:: sh

   pip install dlinfo
   # or
   pipenv install dlinfo

Usage
-----

.. code:: python

   >>> from dlinfo import DLInfo
   >>> lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
   >>> dlinfo = DLInfo(lib)
   >>> dlinfo.path
   '/lib/x86_64-linux-gnu/libc.so.6'
