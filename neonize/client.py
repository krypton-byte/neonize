from __future__ import annotations
from ._binder import gocode, func_bytes, func_string
from typing import Optional, Callable
import typing
import magic
import ctypes
from PIL import Image
from io import BytesIO
from .proto.Neonize_pb2 import (
    MessageInfo,
    MessageSource,
    JID,
    UploadReturnFunction,
    GroupInfo,
    JoinGroupWithLinkReturnFunction,
    GetGroupInviteLinkReturnFunction,
    GetGroupInfoReturnFunction,
    DownloadReturnFunction,
    SendMessageReturnFunction,
    UploadResponse
)
from .proto import Neonize_pb2 as neonize_proto
from .proto.def_pb2 import Message, StickerMessage, ExtendedTextMessage, ContextInfo
from .utils import MediaType, Jid2String, get_bytes_from_name_or_url, ChatPresence, ChatPresenceMedia
from .exc import InvalidInviteLink, DownloadError, UploadError


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

    def send_message(
        self, to: JID, message: typing.Union[Message, str]
    ) -> SendMessageReturnFunction:
        to_bytes = to.SerializeToString()
        if isinstance(message, str):
            message_bytes = Message(conversation=message).SerializeToString()
        else:
            message_bytes = message.SerializeToString()
        sendresponse = self.__client.SendMessage(
            self.uuid, to_bytes, len(to_bytes), message_bytes, len(message_bytes)
        ).get_bytes()
        return SendMessageReturnFunction.FromString(sendresponse)

    def send_sticker(
        self,
        to: JID,
        file_or_bytes: typing.Union[str | bytes],
        quoted: Optional[Message] = None,
        from_: Optional[MessageSource] = None,
    ) -> SendMessageReturnFunction:
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
        message = Message(
            stickerMessage=StickerMessage(
                url=upload.url,
                directPath=upload.DirectPath,
                fileEncSha256=upload.FileEncSHA256,
                fileLength=upload.FileLength,
                fileSha256=upload.FileSHA256,
                mediaKey=upload.MediaKey,
                mimetype=magic.from_buffer(save, mime=True),
            )
        )
        if quoted and from_:
            message.stickerMessage.contextInfo.MergeFrom(
                ContextInfo(
                    stanzaId=from_.ID,
                    participant=Jid2String(from_.Sender),
                    quotedMessage=message,
                )
            )
        return self.send_message(
            to,
            message,
        )

    def upload(
        self, binary: bytes, media_type: Optional[MediaType] = None
    ) -> UploadResponse:
        if not media_type:
            mime = MediaType.from_magic(binary)
        else:
            mime = media_type
        response = self.__client.Upload(self.uuid, binary, len(binary), mime.value)
        upload_model = UploadReturnFunction.FromString(response.get_bytes())
        if upload_model.Error:
            raise UploadError(upload_model.Error)
        return upload_model.UploadResponse

    def download(
        self, message: Message, path: Optional[str] = None
    ) -> Union[None, bytes]:
        msg_protobuf = message.SerializeToString()
        media_buff = self.__client.Download(
            self.uuid, msg_protobuf, len(msg_protobuf)
        ).get_bytes()
        media = DownloadReturnFunction.FromString(media_buff)
        if media.Error:
            raise DownloadException(media.Error)
        if path:
            with open(path, "wb") as file:
                file.write(media.binary)
        else:
            return media.Binary
    def send_chat_presence(self, jid: JID, state: ChatPresence, media: ChatPresenceMedia) -> str:
        jidbyte = jid.SerializeToString()
        return self.__client.SendChatPresence(
            self.uuid,
            jidbyte,
            len(jidbyte),
            state.value,
            media.value
        ).decode()
    def get_group_info(self, jid: JID) -> GetGroupInfoReturnFunction:
        jidbuf = jid.SerializeToString()
        group_info_buf = self.__client.GetGroupInfo(
            self.uuid,
            jidbuf,
            len(jidbuf),
        )
        return GetGroupInfoReturnFunction.FromString(group_info_buf.get_bytes())

    def set_group_name(self, jid: JID, name: str):
        jidbuf = jid.SerializeToString()
        self.__client.SetGroupName(
            self.uuid, jidbuf, len(jidbuf), ctypes.create_string_buffer(name.encode())
        )

    def set_group_photo(self, jid: JID, file_or_bytes: typing.Union[str, bytes]):
        data = get_bytes_from_name_or_url(file_or_bytes)
        jid_buf = jid.SerializeToString()
        print("send grup photo")
        response = self.__client.SetGroupPhoto(
            self.uuid, jid_buf, len(jid_buf), data, len(data)
        )
        return response.decode()

    def leave_group(self, jid: JID) -> str:
        jid_buf = jid.SerializeToString()
        return self.__client.LeaveGroup(self.uuid, jid_buf, len(jid_buf)).decode()

    def get_group_invite_link(self, jid: JID, revoke: bool = False) -> str:
        jid_buf = jid.SerializeToString()
        response = self.__client.GetGroupInviteLink(
            self.uuid, jid_buf, len(jid_buf), revoke
        ).get_bytes()
        return GetGroupInviteLinkReturnFunction.FromString(response)

    def join_group_with_link(self, code: str) -> JoinGroupWithLinkReturnFunction:
        resp = self.__client.JoinGroupWithLink(self.uuid, code.encode()).get_bytes()
        print("result", resp)
        return JoinGroupWithLinkReturnFunction.FromString(resp)

    def connect(self):
        self.__client.Neonize(
            ctypes.create_string_buffer(self.name.encode()),
            ctypes.create_string_buffer(self.uuid),
            func_string(self.__onQr),
            func_bytes(self.__onLoginStatus),
            func_bytes(self.__onMessage),
        )
