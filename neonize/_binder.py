import ctypes
from pathlib import Path

gocode = ctypes.CDLL((Path(__file__).parent / "gocode/gocode.so"))
func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
func_bytes = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int
)


class Bytes(ctypes.Structure):
    ptr: int
    size: int
    _fields_ = [("ptr", ctypes.POINTER(ctypes.c_char)), ("size", ctypes.c_size_t)]

    def get_bytes(self):
        return ctypes.string_at(self.ptr, self.size)


gocode.Upload.restype = Bytes
gocode.Download.restype = Bytes
gocode.GetGroupInfo.restype = Bytes
gocode.SetGroupPhoto.restype = ctypes.c_char_p
gocode.LeaveGroup.restype = ctypes.c_char_p
gocode.SetGroupName.restype = ctypes.c_char_p
gocode.GetGroupInviteLink.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_bool,
]
gocode.GetGroupInviteLink.restype = Bytes
gocode.JoinGroupWithLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
gocode.JoinGroupWithLink.restype = Bytes
gocode.SendMessage.restype = Bytes
gocode.SendChatPresence.restype = ctypes.c_char_p
gocode.BuildRevoke.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
]
gocode.BuildRevoke.restype = Bytes
