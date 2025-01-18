from .proto import Neonize_pb2 as neonize
from .proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    ProtocolMessage,
    PeerDataOperationRequestMessage,
    PeerDataOperationRequestType,
)
from .proto.waCommon.WACommon_pb2 import MessageKey
from .const import DEFAULT_USER_SERVER
from .utils.jid import Jid2String, JIDToNonAD
import time


def build_edit(chat: neonize.JID, message_id: str, new_message: Message) -> Message:
    """
    This function builds an edited message in the WhatsApp protocol format.

    :param chat: The JID (Jabber ID) of the chat where the message will be sent.
    :type chat: neonize.JID
    :param message_id: The unique identifier of the message to be edited.
    :type message_id: str
    :param new_message: The new message content that will replace the old message.
    :type new_message: waProto.Message
    :return: The constructed message in the WhatsApp protocol format.
    :rtype: waProto.Message
    """
    return Message(
        editedMessage=FutureProofMessage(
            message=Message(
                protocolMessage=ProtocolMessage(
                    key=MessageKey(
                        fromMe=True,
                        ID=message_id,
                        remoteJID=Jid2String(chat),
                    ),
                    type=ProtocolMessage.MESSAGE_EDIT,
                    editedMessage=new_message,
                    timestampMS=int(time.time() * 1000),
                )
            )
        )
    )


def build_revoke(chat: neonize.JID, sender: neonize.JID, id: str, myJID: neonize.JID) -> Message:
    """
    This function builds and returns a protocol message of type 'REVOKE' with given parameters.

    :param chat: The chat ID where the message is to be revoked
    :type chat: neonize.JID
    :param sender: The sender's ID who is revoking the message
    :type sender: neonize.JID
    :param id: The ID of the message to be revoked
    :type id: str
    :param myJID: The ID of the user using the application
    :type myJID: neonize.JID
    :return: A protocol message of type 'REVOKE'
    :rtype: waProto.Message
    """
    msgKey = MessageKey(
        fromMe=myJID.User == sender.User,
        ID=id,
        remoteJID=Jid2String(chat),
    )
    if not sender.IsEmpty and not msgKey.fromMe and chat.Server != DEFAULT_USER_SERVER:
        msgKey.participant = Jid2String(JIDToNonAD(sender))
    return Message(protocolMessage=ProtocolMessage(type=ProtocolMessage.REVOKE, key=msgKey))


def build_history_sync_request(message_info: neonize.MessageInfo, count: int) -> Message:
    """
    Builds a history sync request message.

    :param message_info: Information about the message to sync from.
    :type message_info: neonize.MessageInfo
    :param count: Number of messages to sync.
    :type count: int
    :return: A constructed Message object for history sync.
    :rtype: Message
    """
    return Message(
        protocolMessage=ProtocolMessage(
            type=ProtocolMessage.PEER_DATA_OPERATION_REQUEST_MESSAGE,
            peerDataOperationRequestMessage=PeerDataOperationRequestMessage(
                peerDataOperationRequestType=PeerDataOperationRequestType.HISTORY_SYNC_ON_DEMAND,
                historySyncOnDemandRequest=PeerDataOperationRequestMessage.HistorySyncOnDemandRequest(
                    chatJID=Jid2String(message_info.MessageSource.Chat),
                    oldestMsgID=message_info.ID,
                    oldestMsgFromMe=message_info.MessageSource.IsFromMe,
                    onDemandMsgCount=count,
                    oldestMsgTimestampMS=message_info.Timestamp,
                ),
            ),
        )
    )
