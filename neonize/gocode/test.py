import ctypes
import time
import segno
gocode = ctypes.CDLL("./gocode.so")
func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
func_bytes = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int,ctypes.c_void_p, ctypes.c_int)
import signal, sys
from def_pb2 import Message, ImageMessage, ContextInfo
from Neonize_pb2 import MessageSource, UploadResponse, JID
signal.signal(signal.SIGINT, lambda x:sys.exit(0))
uid = ctypes.create_string_buffer(b"mysession")

class Bytes(ctypes.Structure):
    _fields_ = [
        ('ptr', ctypes.POINTER(ctypes.c_char)),
        ('size', ctypes.c_size_t)
    ]
    def get_bytes(self):
        return ctypes.string_at(self.ptr, self.size)

gocode.Upload.restype = Bytes
def callback_login_status(s: str):
    print(ctypes.string_at(s), 'loggin')

def callback_qr(s: str):
    print(segno.make_qr(ctypes.string_at(s)).terminal())

def on_message(b: int, size: int, message_info_byte: int, message_info_size: int):
    d=ctypes.string_at(b, size)
    print(d)
    msg: Message=Message.FromString(d)
    message_source_bytes = ctypes.string_at(message_info_byte, message_info_size)
    message_source: MessageSource=MessageSource.FromString(message_source_bytes)
    new_message = Message(conversation="PONGGGGG").SerializeToString()
    print(message_source.Chat, 'chat')
    chat = message_source.Chat.SerializePartialToString()
    if msg.extendedTextMessage and msg.extendedTextMessage.text == "ping":
        gocode.SendMessage(uid, chat, len(chat), new_message, len(new_message))
    elif msg.extendedTextMessage and msg.extendedTextMessage.text == "image":
        imgbuff = open('gg.jpeg','rb').read()
        resp = gocode.Upload(uid, imgbuff, len(imgbuff), 1)
        upresp: UploadResponse=UploadResponse.FromString(resp.get_bytes())
        msg_photo = Message(
            imageMessage=ImageMessage(
                url=upresp.url,
                thumbnailDirectPath=upresp.DirectPath,
                thumbnailSha256=upresp.FileSHA256,
                thumbnailEncSha256=upresp.FileEncSHA256,
                mimetype="image/jpeg",
                caption="test python",
                fileSha256=upresp.FileSHA256,
                fileEncSha256=upresp.FileEncSHA256,
                fileLength=len(imgbuff),
                jpegThumbnail=imgbuff,
                directPath=upresp.DirectPath,
                contextInfo=ContextInfo(
                    stanzaId=message_source.ID,
                    participant=Jid2String(message_source.Sender),
                    quotedMessage=msg

                ),
                mediaKey=upresp.MediaKey
            )
        ).SerializeToString()
        gocode.SendMessage(
            uid, chat, len(chat),msg_photo, len(msg_photo)
        )

def Jid2String(jid: JID) -> str:
    if jid.RawAgent > 0:
        return "%s.%s:%d@%s" %(
            jid.User,
            jid.RawAgent,
            jid.Device,
            jid.Server
        )
    elif jid.Device > 0:
        return "%s:%d@%s" % (jid.User, jid.Device, jid.Server)
    elif len(jid.User) > 0:
        return "%s@%s" % (jid.User, jid.Server)
    return jid.Server
gocode.Neonize(
    ctypes.create_string_buffer(b"krypton"),
    uid,
    func_string(callback_qr),
    func_string(callback_login_status),
    func_bytes(on_message)
)