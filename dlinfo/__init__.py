__all__ = ['DLInfo']

import sys

if sys.platform == 'darwin':
    from ._macosx import DLInfo
else:
    from ._glibc import DLInfo
