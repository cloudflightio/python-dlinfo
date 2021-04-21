import builtins
import os
import platform
import re
import unittest.mock


def dyld_find_mock(lib_filename):
    # https://github.com/python/cpython/blob/master/Lib/ctypes/macholib/dyld.py#L116
    lib_name = re.match(r'^(lib\w+)\.\w+(\.\d+)?$', lib_filename).group(1)
    return os.path.join(os.sep, 'usr', 'lib', lib_name + '.dylib')

_BUILTIN_IMPORT = builtins.__import__

def import_mock(name, *args, **kwargs):
    if name == 'ctypes.macholib.dyld' and platform.system() != 'Darwin':
        dyld_module = unittest.mock.MagicMock()
        dyld_module.dyld_find = dyld_find_mock
        return dyld_module
    return _BUILTIN_IMPORT(name, *args, **kwargs)

# required for tests/dlinfo_macosx_mock_test.py and doctests in dlinfo/_macosx.py.
# @pytest.fixture(autouse=True) does not run before import statements.
builtins.__import__ = import_mock
