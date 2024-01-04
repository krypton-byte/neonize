from .proto import Neonize_pb2 as neonize, def_pb2 as waProto
from .const import DEFAULT_USER_SERVER
from .utils.jid import Jid2String, JIDToNonAD
import time


def build_edit(
    chat: neonize.JID, message_id: str, new_message: waProto.Message
) -> waProto.Message:
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
