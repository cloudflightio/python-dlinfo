import ctypes
import ctypes.util
import importlib
import os
import types
import unittest.mock

import pytest

import dlinfo


# pylint: disable=redefined-outer-name
@pytest.fixture
def dlinfo_module_mac() -> types.ModuleType:
    with unittest.mock.patch('sys.platform', 'darwin'):
        dlinfo_module = importlib.reload(dlinfo)
    assert dlinfo_module.DLInfo.__module__ == 'dlinfo._macosx'
    return dlinfo_module


@pytest.mark.parametrize('lib_name', [
    'SegFault',
    'c',
    'dl',
    'python_grasp',
])
def test_dlinfo_path(dlinfo_module_mac, lib_name):
    lib_filename = ctypes.util.find_library(lib_name)
    if not lib_filename:
        pytest.xfail(f"lib{lib_name} not found")
    lib = ctypes.cdll.LoadLibrary(lib_filename)
    lib_info = dlinfo_module_mac.DLInfo(lib)
    if os.path.exists(lib_info.path): # mac
        assert os.path.isabs(lib_info.path)
        assert lib_filename == os.path.basename(lib_info.path)
    else: # dyld_find mock
        assert lib_info.path == f"/usr/lib/lib{lib_name}.dylib"
