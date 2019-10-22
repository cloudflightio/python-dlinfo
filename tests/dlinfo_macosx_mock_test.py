import builtins
import ctypes
import ctypes.util
import os
import types
import unittest.mock

import pytest

BUILTIN_IMPORT = builtins.__import__


def dyld_find_mock(name):
    # https://github.com/python/cpython/blob/master/Lib/ctypes/macholib/dyld.py#L116
    return os.path.join(os.sep, 'lib', name)


def import_mock(name, *args):
    if name == 'ctypes.macholib.dyld':
        dyld_module = unittest.mock.MagicMock()
        dyld_module.dyld_find = dyld_find_mock
        return dyld_module
    return BUILTIN_IMPORT(name, *args)


@pytest.fixture
def dlinfo_module_mac() -> types.ModuleType:
    with unittest.mock.patch('sys.platform', 'darwin'):
        with unittest.mock.patch('builtins.__import__', import_mock):
            dlinfo_module = __import__('dlinfo')
    assert dlinfo_module.DLInfo.__module__ == 'dlinfo._macosx'
    return dlinfo_module


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
