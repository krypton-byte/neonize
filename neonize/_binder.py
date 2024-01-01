import ctypes
from pathlib import Path
gocode = ctypes.CDLL((Path(__file__).parent / 'gocode/gocode.so'))
func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
func_bytes = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int,ctypes.c_void_p, ctypes.c_int)
class Bytes(ctypes.Structure):
    _fields_ = [
        ('ptr', ctypes.POINTER(ctypes.c_char)),
        ('size', ctypes.c_size_t)
    ]
    def get_bytes(self):
        return ctypes.string_at(self.ptr, self.size)
gocode.Upload.restype = Bytes
gocode.Download.restype = Bytes