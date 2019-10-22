import ctypes
import ctypes.util
import os
import sys
import unittest.mock

import pytest


def dyld_find_mock(name):
    # https://github.com/python/cpython/blob/master/Lib/ctypes/macholib/dyld.py#L116
    return os.path.join(os.sep, 'lib', name)


@pytest.fixture
def dlinfo_module_mac():
    with unittest.mock.patch('sys.platform', 'darwin'):
        sys.modules['ctypes.macholib.dylib'] = unittest.mock.Mock()
        sys.modules['ctypes.macholib.dylib'].dyld_find = dyld_find_mock
        return __import__('dlinfo')


@pytest.mark.parametrize('lib_name', [
    'c',
    'dl',
    'python_grasp',
])
def test_dlinfo_path(dlinfo_module_mac, lib_name):
    lib_filename = ctypes.util.find_library(lib_name)
    if not lib_filename:
        pytest.xfail('lib{} not found'.format(lib_name))
    lib = ctypes.cdll.LoadLibrary(lib_filename)
    dlinfo = dlinfo_module_mac.DLInfo(lib)
    assert lib_filename == os.path.basename(dlinfo.path)
    assert os.path.join(os.sep, 'lib') == os.path.dirname(dlinfo.path)
