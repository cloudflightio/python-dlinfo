import ctypes
import ctypes.util
import sys

# dlfcn.h
_RTLD_DI_LINKMAP = 2


class _LinkMap(ctypes.Structure):
    # link.h
    _fields_ = [
        ('l_addr', ctypes.c_void_p),
        ('l_name', ctypes.c_char_p),
        ('l_ld', ctypes.c_void_p),
        ('l_next', ctypes.c_void_p),
        ('l_previous', ctypes.c_void_p),
    ]


_LIBDL = ctypes.cdll.LoadLibrary(ctypes.util.find_library('dl'))
_DLINFO = _LIBDL.dlinfo
_DLINFO.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p
_DLINFO.restype = ctypes.c_int


class DLInfo:

    def __init__(self, cdll: ctypes.CDLL):
        self._linkmap = ctypes.c_void_p()
        # pylint: disable=protected-access
        if _DLINFO(cdll._handle, _RTLD_DI_LINKMAP, ctypes.byref(self._linkmap)) != 0:
            raise Exception('dlinfo on {} failed'.format(cdll._name))

    @property
    def path(self) -> str:
        return ctypes.cast(self._linkmap, ctypes.POINTER(_LinkMap)).contents.l_name \
            .decode(sys.getdefaultencoding())
