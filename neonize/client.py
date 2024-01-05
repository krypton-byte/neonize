from __future__ import annotations

import ctypes
import typing
from io import BytesIO
from typing import Optional, Callable, List

import magic
from PIL import Image

from ._binder import gocode, func_bytes, func_string
from .builder import build_edit, build_revoke
from .exc import (
    DownloadError,
    UploadError,
    InviteLinkError,
    GetGroupInfoError,
    SetGroupPhotoError,
    GetGroupInviteLinkError,
    CreateGroupError,
    IsOnWhatsAppError,
    GetUserInfoError,
    SendMessageError,
    BuildPollVoteError,
    CreateNewsletterError,
    FollowNewsletterError,
    GetBlocklistError
)
from .proto import Neonize_pb2 as neonize_proto
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
    UploadResponse,
    SetGroupPhotoReturnFunction,
    ReqCreateGroup,
    GroupLinkedParent,
    GroupParent,
    IsOnWhatsAppReturnFunction,
    IsOnWhatsAppResponse,
    JIDArray,
    GetUserInfoReturnFunction,
    GetUserInfoSingleReturnFunction,
    SendResponse,
    Device,
)
from .proto.def_pb2 import Message, StickerMessage, ContextInfo
from .utils import (
    MediaType,
    Jid2String,
    get_bytes_from_name_or_url,
    ChatPresence,
    ChatPresenceMedia,
)


class NewClient:
    def __init__(
            self,
            name: str,
            qrCallback: Optional[Callable[[NewClient, bytes], None]] = None,
            messageCallback: Optional[
                Callable[[NewClient, neonize_proto.Message], None]
            ] = None,
            uuid: Optional[str] = None,
    ):
        """Initializes a new client instance.

        :param name: The name or identifier for the new client.
        :type name: str
        :param qrCallback: Optional. A callback function for handling QR code updates, defaults to None.
        :type qrCallback: Optional[Callable[[NewClient, bytes], None]], optional
        :param messageCallback: Optional. A callback function for handling incoming messages, defaults to None.
        :type messageCallback: Optional[Callable[[NewClient, MessageSource, Message], None]], optional
        :param uuid: Optional. A unique identifier for the client, defaults to None.
        :type uuid: Optional[str], optional
        """
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
    ):
        """Handles incoming messages.

        :param message_protobytes: The bytes representing the message.
        :type message_protobytes: int
        :param message_size: The size of the message in bytes.
        :type message_size: int
        :param message_source: The source of the message.
        :type message_source: int
        :param message_source_size: The size of the message source.
        :type message_source_size: int
        """
        if self.messageCallback:
            bytes_data = ctypes.string_at(message_protobytes, message_size)
            self.messageCallback(self, neonize_proto.Message.FromString(bytes_data))

    def send_message(
            self, to: JID, message: typing.Union[Message, str]
    ) -> SendResponse:
        """Send a message to the specified JID.

        :param to: The JID to send the message to.
        :type to: JID
        :param message: The message to send.
        :type message: typing.Union[Message, str]
        :raises SendMessageError: If there was an error sending the message.
        :return: The response from the server.
        :rtype: SendResponse
        """
        to_bytes = to.SerializeToString()
        if isinstance(message, str):
            message_bytes = Message(conversation=message).SerializeToString()
        else:
            message_bytes = message.SerializeToString()
        sendresponse = self.__client.SendMessage(
            self.uuid, to_bytes, len(to_bytes), message_bytes, len(message_bytes)
        ).get_bytes()
        model = SendMessageReturnFunction.FromString(sendresponse)
        if model.Error:
            raise SendMessageError(model.Error)
        return model.SendResponse

    def edit_message(
            self, chat: JID, message_id: str, new_message: Message
    ) -> SendResponse:
        """Edit a message.

        :param chat: Chat ID
        :type chat: JID
        :param message_id: Message ID
        :type message_id: str
        :param new_message: New message
        :type new_message: Message
        :return: Response from server
        :rtype: SendResponse
        """
        return self.send_message(chat, build_edit(chat, message_id, new_message))

    def revoke_message(self, chat: JID, sender: JID, message_id: str) -> SendResponse:
        """Revoke a message.

        :param chat: Chat ID
        :type chat: JID
        :param sender: Sender ID
        :type sender: JID
        :param message_id: Message ID
        :type message_id: str
        :return: Response from server
        :rtype: SendResponse
        """
        return self.send_message(chat, self.build_revoke(chat, sender, message_id))

    def build_poll_vote_creation(
            self, name: str, options: List[str], selectable_count: int
    ) -> Message:
        """Build a poll vote creation message.
        
        :param name: The name of the poll.
        :type name: str
        :param options: The options for the poll.
        :type options: List[str]
        :param selectable_count: The number of selectable options.
        :type selectable_count: int
        :return: The poll vote creation message.
        :rtype: Message
        """
        options_buf = neonize_proto.ArrayString(data=options).SerializeToString()
        return Message.FromString(
            self.__client.BuildPollVoteCreation(
                self.uuid,
                name.encode(),
                options_buf,
                len(options_buf),
                selectable_count,
            ).get_bytes()
        )

    def build_poll_vote(
            self, poll_info: MessageInfo, option_names: List[str]
    ) -> Message:
        """
        Builds a poll vote.

        :param poll_info: The information about the poll.
        :type poll_info: MessageInfo
        :param option_names: The names of the options to vote for.
        :type option_names: List[str]
        :return: The poll vote message.
        :rtype: Message
        :raises BuildPollVoteError: If there is an error building the poll vote.
        """
        option_names_proto = neonize_proto.ArrayString(
            data=option_names
        ).SerializeToString()
        poll_info_proto = poll_info.SerializeToString()
        resp = self.__client.BuildPollVote(
            self.uuid,
            poll_info_proto,
            len(poll_info_proto),
            option_names_proto,
            len(option_names_proto),
        ).get_bytes()
        model = neonize_proto.BuildPollVoteReturnFunction.FromString(resp)
        if model.Error:
            raise BuildPollVoteError(model.Error)
        return model.PollVote

    def build_reaction(
            self, chat: JID, sender: JID, message_id: str, reaction: str
    ) -> Message:
        sender_proto = sender.SerializeToString()
        chat_proto = chat.SerializeToString()
        return Message.FromString(
            self.__client.BuildReaction(
                self.uuid,
                chat_proto,
                len(chat_proto),
                sender_proto,
                len(sender_proto),
                message_id.encode(),
                reaction.encode(),
            ).get_bytes()
        )

    def build_revoke(
            self, chat: JID, sender: JID, message_id: str, with_go: bool = False
    ) -> Message:
        """Builds a message to revoke a previous message.

        :param chat: The JID (Jabber Identifier) of the chat where the message should be revoked.
        :type chat: JID
        :param sender: The JID of the sender of the message to be revoked.
        :type sender: JID
        :param message_id: The unique identifier of the message to be revoked.
        :type message_id: str
        :return: The constructed Message object for revoking the specified message.
        :rtype: Message
        """
        if with_go:
            chat_buf = chat.SerializeToString()
            sender_buf = sender.SerializeToString()
            return Message.FromString(
                self.__client.BuildRevoke(
                    self.uuid,
                    chat_buf,
                    len(chat_buf),
                    sender_buf,
                    len(sender_buf),
                    message_id.encode(),
                ).get_bytes()
            )
        else:
            return build_revoke(chat, sender, message_id, self.get_me().JID)

    def send_sticker(
            self,
            to: JID,
            file_or_bytes: typing.Union[str, bytes],
            quoted: Optional[Message] = None,
            from_: Optional[MessageSource] = None,
    ) -> SendMessageReturnFunction:
        """Sends a sticker to the specified recipient.

        :param to: The JID (Jabber Identifier) of the recipient.
        :type to: JID
        :param file_or_bytes: Either a file path (str) or binary data (bytes) representing the sticker.
        :type file_or_bytes: typing.Union[str | bytes]
        :param quoted: Optional. The message to which the sticker is a reply. Defaults to None.
        :type quoted: Optional[Message], optional
        :param from_: Optional. The source information of the sender. Defaults to None.
        :type from_: Optional[MessageSource], optional
        :return: A function for handling the result of the sticker sending process.
        :rtype: SendMessageReturnFunction
        """
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
        """Uploads media content.

        :param binary: The binary data to be uploaded.
        :type binary: bytes
        :param media_type: Optional. The media type of the binary data, defaults to None.
        :type media_type: Optional[MediaType], optional
        :raises UploadError: Raised if there is an issue with the upload.
        :return: An UploadResponse containing information about the upload.
        :rtype: UploadResponse
        """
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
    ) -> typing.Union[None, bytes]:
        """Downloads content from a message.

        :param message: The message containing the content to download.
        :type message: Message
        :param path: Optional. The local path to save the downloaded content, defaults to None.
        :type path: Optional[str], optional
        :raises DownloadException: Raised if there is an issue with the download.
        :return: The downloaded content as bytes, or None if the content is not available.
        :rtype: Union[None, bytes]
        """
        msg_protobuf = message.SerializeToString()
        media_buff = self.__client.Download(
            self.uuid, msg_protobuf, len(msg_protobuf)
        ).get_bytes()
        media = DownloadReturnFunction.FromString(media_buff)
        if media.Error:
            raise DownloadError(media.Error)
        if path:
            with open(path, "wb") as file:
                file.write(media.binary)
        else:
            return media.Binary

    def generate_message_id(self) -> str:
        """Generates a unique identifier for a message.

        :return: A string representing the unique identifier for the message.
        :rtype: str
        """
        return self.__client.GenerateMessageID(self.uuid).decode()

    def send_chat_presence(
            self, jid: JID, state: ChatPresence, media: ChatPresenceMedia
    ) -> str:
        """Sends chat presence information.

        :param jid: The JID (Jabber Identifier) of the chat.
        :type jid: JID
        :param state: The chat presence state.
        :type state: ChatPresence
        :param media: The chat presence media information.
        :type media: ChatPresenceMedia
        :return: A string indicating the result or status of the presence information sending.
        :rtype: str
        """
        jidbyte = jid.SerializeToString()
        return self.__client.SendChatPresence(
            self.uuid, jidbyte, len(jidbyte), state.value, media.value
        ).decode()

    def is_on_whatsapp(self, numbers: List[str] = []) -> IsOnWhatsAppResponse:
        """Check if the provided phone numbers are on WhatsApp.

        :param numbers: List of phone numbers to check. Defaults to [].
        :type numbers: List[str], optional
        :raises IsOnWhatsAppError: Raised if there is an error while checking.
        :return: A response object containing information about WhatsApp presence.
        :rtype: IsOnWhatsAppResponse
        """
        if numbers:
            numbers_buf = " ".join(numbers).encode()
            response = self.__client.IsOnWhatsApp(
                self.uuid, numbers_buf, len(numbers_buf)
            ).get_bytes()
            model = IsOnWhatsAppReturnFunction.FromString(response)
            if model.Error:
                raise IsOnWhatsAppError(model.Error)
            return model.IsOnWhatsAppResponse
        return []

    @property
    def is_connected(self) -> bool:
        """Check if the object is currently connected.

        :return: True if the object is connected, False otherwise.
        :rtype: bool
        """
        return self.__client.IsConnected(self.uuid)

    @property
    def is_logged_in(self) -> bool:
        """Check if the user is currently logged in.

        :return: True if the user is logged in, False otherwise.
        :rtype: bool
        """
        return self.__client.IsLoggedIn(self.uuid)

    def get_user_info(self, jid: List[JID]) -> GetUserInfoSingleReturnFunction:
        """Retrieve information for the provided JIDs.

        :param jid: List of JIDs (Jabber IDs) for which to retrieve information.
        :type jid: List[JID]
        :raises GetUserInfoError: Raised if there is an error while retrieving user information.
        :return: A function providing information for the specified JIDs.
        :rtype: GetUserInfoSingleReturnFunction
        """
        jidbuf = JIDArray(JIDS=jid).SerializeToString()
        getUser = self.__client.GetUserInfo(self.uuid, jidbuf, len(jidbuf)).get_bytes()
        model = GetUserInfoReturnFunction.FromString(getUser)
        if model.Error:
            raise GetUserInfoError(model.Error)
        return model.UsersInfo

    def get_group_info(self, jid: JID) -> GroupInfo:
        """Retrieves information about a group.

        :param jid: The JID (Jabber Identifier) of the group.
        :type jid: JID
        :raises GetGroupInfoError: Raised if there is an issue retrieving group information.
        :return: Information about the specified group.
        :rtype: GroupInfo
        """
        jidbuf = jid.SerializeToString()
        group_info_buf = self.__client.GetGroupInfo(
            self.uuid,
            jidbuf,
            len(jidbuf),
        )
        model = GetGroupInfoReturnFunction.FromString(group_info_buf.get_bytes())
        if model.Error:
            raise GetGroupInfoError(model.Error)
        return model.GroupInfo

    def set_group_name(self, jid: JID, name: str) -> str:
        """Sets the name of a group.

        :param jid: The JID (Jabber Identifier) of the group.
        :type jid: JID
        :param name: The new name to be set for the group.
        :type name: str
        :return: A string indicating the result or an error status. Empty string if successful.
        :rtype: str
        """
        jidbuf = jid.SerializeToString()
        return self.__client.SetGroupName(
            self.uuid, jidbuf, len(jidbuf), ctypes.create_string_buffer(name.encode())
        ).decode()

    def set_group_photo(self, jid: JID, file_or_bytes: typing.Union[str, bytes]) -> str:
        """Sets the photo of a group.

        :param jid: The JID (Jabber Identifier) of the group.
        :type jid: JID
        :param file_or_bytes: Either a file path (str) or binary data (bytes) representing the group photo.
        :type file_or_bytes: typing.Union[str, bytes]
        :raises SetGroupPhotoError: Raised if there is an issue setting the group photo.
        :return: A string indicating the result or an error status.
        :rtype: str
        """
        data = get_bytes_from_name_or_url(file_or_bytes)
        jid_buf = jid.SerializeToString()
        response = self.__client.SetGroupPhoto(
            self.uuid, jid_buf, len(jid_buf), data, len(data)
        )
        model = SetGroupPhotoReturnFunction.FromString(response.get_bytes())
        if model.Error:
            raise SetGroupPhotoError(model.Error)
        return model.PictureID

    def leave_group(self, jid: JID) -> str:
        """Leaves a group.

        :param jid: The JID (Jabber Identifier) of the target group.
        :type jid: JID
        :return: A string indicating the result or an error status. Empty string if successful.
        :rtype: str
        """
        jid_buf = jid.SerializeToString()
        return self.__client.LeaveGroup(self.uuid, jid_buf, len(jid_buf)).decode()

    def get_group_invite_link(self, jid: JID, revoke: bool = False) -> str:
        """Gets or revokes the invite link for a group.

        :param jid: The JID (Jabber Identifier) of the group.
        :type jid: JID
        :param revoke: Optional. If True, revokes the existing invite link; if False, gets the invite link. Defaults to False.
        :type revoke: bool, optional
        :raises GetGroupInviteLinkError: Raised if there is an issue getting or revoking the invite link.
        :return: The group invite link or an error status.
        :rtype: str
        """
        jid_buf = jid.SerializeToString()
        response = self.__client.GetGroupInviteLink(
            self.uuid, jid_buf, len(jid_buf), revoke
        ).get_bytes()
        model = GetGroupInviteLinkReturnFunction.FromString(response)
        if model.Error:
            raise GetGroupInviteLinkError(model.Error)
        return model.InviteLink

    def join_group_with_link(self, code: str) -> JID:
        """Join a group using an invite link.

        :param code: The invite code or link for joining the group.
        :type code: str
        :raises InviteLinkError: Raised if the group membership is pending approval or if the link is invalid.
        :return: The JID (Jabber Identifier) of the joined group.
        :rtype: JID
        """
        resp = self.__client.JoinGroupWithLink(self.uuid, code.encode()).get_bytes()
        model = JoinGroupWithLinkReturnFunction.FromString(resp)
        if model.Error:
            raise InviteLinkError(model.Error)
        return model.Jid

    def create_group(
            self,
            name: str,
            participants: List[JID] = [],
            linked_parent: Optional[GroupLinkedParent] = None,
            group_parent: Optional[GroupParent] = None,
    ) -> GroupInfo | CreateGroupError:
        """Create a new group.

        :param name: The name of the new group.
        :type name: str
        :param participants: Optional. A list of participant JIDs (Jabber Identifiers) to be included in the group. Defaults to an empty list.
        :type participants: List[JID], optional
        :param linked_parent: Optional. Information about a linked parent group, if applicable. Defaults to None.
        :type linked_parent: Optional[GroupLinkedParent], optional
        :param group_parent: Optional. Information about a parent group, if applicable. Defaults to None.
        :type group_parent: Optional[GroupParent], optional
        :return: Information about the newly created group.
        :rtype: GroupInfo
        """
        group_info = ReqCreateGroup(
            name=name, Participants=participants, CreateKey=self.generate_message_id()
        )
        if linked_parent:
            group_info.GroupLinkedParent = linked_parent
        if group_parent:
            group_info.GroupParent = group_parent
        group_info_buf = group_info.SerializeToString()
        resp = self.__client.CreateGroup(self.uuid, group_info_buf, len(group_info_buf))
        model = GetGroupInfoReturnFunction.FromString(resp.get_bytes())
        if model.Error:
            return CreateGroupError(model.Error)
        return model.GroupInfo

    def create_newsletter(
            self, name: str, description: str, picture: typing.Union[str, bytes]
    ) -> neonize_proto.NewsletterMetadata:
        """Create a newsletter with the given name, description, and picture.

        :param name: The name of the newsletter.
        :type name: str
        :param description: The description of the newsletter.
        :type description: str
        :param picture: The picture of the newsletter. It can be either a URL or bytes.
        :type picture: Union[str, bytes]
        :return: The metadata of the created newsletter.
        :rtype: NewsletterMetadata
        :raises CreateNewsletterError: If there is an error creating the newsletter.
        """
        protobuf = neonize_proto.CreateNewsletterParams(
            Name=name,
            Description=description,
            Picture=get_bytes_from_name_or_url(picture),
        ).SerializeToString()
        model = neonize_proto.CreateNewsLetterReturnFunction.FromString(
            self.__client.CreateNewsletter(
                self.uuid, protobuf, len(protobuf)
            ).get_bytes()
        )
        if model.Error:
            raise CreateNewsletterError(model.Error)
        return model.NewsletterMetadata

    def follow_newsletter(self, jid: JID):
        """Follows a newsletter with the given JID.

        :param jid: The JID of the newsletter to follow.
        :type jid: JID
        :return: The error message, if any.
        :rtype: str
        :raises FollowNewsletterError: If there is an error following the newsletter.
        """
        jidbyte = jid.SerializeToString()
        err = self.__client.FollowNewsletter(self.uuid, jidbyte, len(jidbyte)).decode()
        if err:
            raise FollowNewsletterError(err)
        return err

    def get_blocklist(self) -> neonize_proto.Blocklist:
        """
        Retrieves the blocklist from the client.

        :return: neonize_proto.Blocklist: The retrieved blocklist.
        :raises GetBlocklistError: If there was an error retrieving the blocklist.
        """
        model = neonize_proto.GetBlocklistReturnFunction.FromString(self.__client.GetBlocklist(self.uuid).get_bytes())
        if model.Error:
            raise GetBlocklistError(model.Error)
        return model.Blocklist

    def get_me(self) -> Device:
        return Device.FromString(self.__client.GetMe(self.uuid).get_bytes())

    def connect(self):
        self.__client.Neonize(
            ctypes.create_string_buffer(self.name.encode()),
            ctypes.create_string_buffer(self.uuid),
            func_string(self.__onQr),
            func_bytes(self.__onLoginStatus),
            func_bytes(self.__onMessage),
        )
