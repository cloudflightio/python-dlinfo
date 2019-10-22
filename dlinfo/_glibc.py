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

    """
    >>> lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
    >>> dlinfo = DLInfo(lib)
    >>> dlinfo.path
    '/lib/x86_64-linux-gnu/libc.so.6'
    """

    def __init__(self, cdll: ctypes.CDLL):
        _linkmap = ctypes.c_void_p()
        # pylint: disable=protected-access
        if _DLINFO(cdll._handle, _RTLD_DI_LINKMAP, ctypes.byref(_linkmap)) != 0:  # pragma: no cover
            raise Exception('dlinfo on {} failed'.format(cdll._name))
        self._linkmap = ctypes.cast(_linkmap, ctypes.POINTER(_LinkMap))

    @property
    def path(self) -> str:
        return self._linkmap.contents.l_name.decode(sys.getdefaultencoding())
