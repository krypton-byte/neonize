from .proto import Neonize_pb2 as neonize, def_pb2 as waProto
from .const import DEFAULT_USER_SERVER
from .utils.jid import Jid2String, JIDToNonAD
import time


def build_edit(
    chat: neonize.JID, message_id: str, new_message: waProto.Message
) -> waProto.Message:
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
    return waProto.Message(
        editedMessage=waProto.FutureProofMessage(
            message=waProto.Message(
                protocolMessage=waProto.ProtocolMessage(
                    key=waProto.MessageKey(
                        fromMe=True,
                        id=message_id,
                        remoteJid=Jid2String(chat),
                    ),
                    type=waProto.ProtocolMessage.MESSAGE_EDIT,
                    editedMessage=new_message,
                    timestampMs=int(time.time() * 1000),
                )
            )
        )
    )


def build_revoke(
    chat: neonize.JID, sender: neonize.JID, id: str, myJID: neonize.JID
) -> waProto.Message:
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
    msgKey = waProto.MessageKey(
        fromMe=myJID.User == sender.User,
        id=id,
        remoteJid=Jid2String(chat),
    )
    if not sender.IsEmpty and not msgKey.fromMe and chat.Server != DEFAULT_USER_SERVER:
        msgKey.participant = Jid2String(JIDToNonAD(sender))
    return waProto.Message(
        protocolMessage=waProto.ProtocolMessage(
            type=waProto.ProtocolMessage.REVOKE, key=msgKey
        )
    )


def build_history_sync_request(
    message_info: neonize.MessageInfo, count: int
) -> waProto.Message:
    return waProto.Message(
        protocolMessage=waProto.ProtocolMessage(
            type=waProto.ProtocolMessage.PEER_DATA_OPERATION_REQUEST_MESSAGE,
            peerDataOperationRequestMessage=waProto.PeerDataOperationRequestMessage(
                peerDataOperationRequestType=waProto.PeerDataOperationRequestType.HISTORY_SYNC_ON_DEMAND,
                historySyncOnDemandRequest=waProto.PeerDataOperationRequestMessage.HistorySyncOnDemandRequest(
                    chatJid=Jid2String(message_info.MessageSource.Chat),
                    oldestMsgId=message_info.ID,
                    oldestMsgFromMe=message_info.MessageSource.IsFromMe,
                    onDemandMsgCount=count,
                    oldestMsgTimestampMs=message_info.Timestamp,
                ),
            ),
        )
    )
