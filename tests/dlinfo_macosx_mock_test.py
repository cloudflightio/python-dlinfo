import ctypes
import ctypes.util
import os
import types
import unittest.mock

import pytest


def dyld_find_mock(name):
    # https://github.com/python/cpython/blob/master/Lib/ctypes/macholib/dyld.py#L116
    return os.path.join(os.sep, 'lib', name)


@pytest.fixture
def dlinfo_module_mac() -> types.ModuleType:
    with unittest.mock.patch('sys.platform', 'darwin'):
        dyld_module = unittest.mock.MagicMock()
        dyld_module.dyld_find = dyld_find_mock
        with unittest.mock.patch.dict('sys.modules',
                                      {'ctypes': unittest.mock.MagicMock(),
                                       'ctypes.macholib': unittest.mock.MagicMock(),
                                       'ctypes.macholib.dyld': dyld_module}):
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
