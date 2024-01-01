from __future__ import annotations
from ._binder import gocode, func_bytes, func_string
from typing import Optional, Callable
import typing
import magic
import ctypes
from PIL import Image
from io import BytesIO
from .proto.Neonize_pb2 import MessageInfo, MessageSource, JID, UploadResponse
from .proto.def_pb2 import Message, StickerMessage
from .utils import MediaType


class NewClient:
    def __init__(
        self,
        name: str,
        qrCallback: Optional[Callable[[NewClient, bytes], None]] = None,
        messageCallback: Optional[
            Callable[[NewClient, MessageSource, Message], None]
        ] = None,
        uuid: Optional[str] = None,
    ):
        self.name = name
        self.uuid = (uuid or name).encode()
        self.qrCallback = qrCallback
        self.messageCallback = messageCallback
        self.__client = gocode

    def __onLoginStatus(self, s: str):
        print(s)

    def __onQr(self, qr_protobytes):
        if self.qrCallback:
            self.qrCallback(self, ctypes.string_at(qr_protobytes))

    def __onMessage(
        self,
        message_protobytes: int,
        message_size: int,
        message_source: int,
        message_source_size: int,
    ):
        if self.__onMessage:
            bytes_data = ctypes.string_at(message_protobytes, message_size)
            message_source_data = ctypes.string_at(message_source, message_source_size)
            self.messageCallback(
                self,
                MessageSource.FromString(message_source_data),
                Message.FromString(bytes_data),
            )

    def send_message(self, to: JID, message: Message):
        to_bytes = to.SerializeToString()
        message_bytes = message.SerializeToString()
        self.__client.SendMessage(
            self.uuid, to_bytes, len(to_bytes), message_bytes, len(message_bytes)
        )

    def send_sticker(
        self,
        to: JID,
        file_or_bytes: typing.Union[str | bytes],
        quoted: Optional[Message] = None,
    ):
        if isinstance(file_or_bytes, str):
            with open(file_or_bytes, "rb") as file:
                image_buf = file.read()
        else:
            image_buf = file_or_bytes
        io_save = BytesIO()
        Image.open(BytesIO(image_buf)).convert("RGBA").resize((512, 512)).save(
            io_save, format="webp"
        )
        io_save.seek(0)
        save = io_save.read()
        upload = self.upload(save)
        self.send_message(
            to,
            Message(
                stickerMessage=StickerMessage(
                    url=upload.url,
                    directPath=upload.DirectPath,
                    fileEncSha256=upload.FileEncSHA256,
                    fileLength=upload.FileLength,
                    fileSha256=upload.FileSHA256,
                    mediaKey=upload.MediaKey,
                    mimetype=magic.from_buffer(save, mime=True),
                )
            ),
        )

    def upload(
        self, binary: bytes, media_type: Optional[MediaType] = None
    ) -> UploadResponse:
        if not media_type:
            mime = MediaType.from_magic(binary)
        else:
            mime = media_type
        respose = self.__client.Upload(self.uuid, binary, len(binary), mime.value)
        return UploadResponse.FromString(respose.get_bytes())

    def download(
        self, message: Message, path: Optional[str] = None
    ) -> Union[None, bytes]:
        msg_protobuf = message.SerializeToString()
        media_buff = self.__client.Download(
            self.uuid, msg_protobuf, len(msg_protobuf)
        ).get_bytes()
        if path:
            with open(path, "wb") as file:
                file.write(media_buff)

    def connect(self):
        self.__client.Neonize(
            ctypes.create_string_buffer(self.name.encode()),
            ctypes.create_string_buffer(self.uuid),
            func_string(self.__onQr),
            func_bytes(self.__onLoginStatus),
            func_bytes(self.__onMessage),
        )
