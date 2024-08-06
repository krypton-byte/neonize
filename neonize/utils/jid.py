import copy
from ..proto.Neonize_pb2 import JID


def JIDToNonAD(jid: JID) -> JID:
    """
    Converts a JID (Jabber ID) to a non-AD (Active Directory) format by setting RawAgent and Device to 0.

    :param jid: The JID to be converted.
    :type jid: JID
    :return: A new JID object with RawAgent and Device set to 0.
    :rtype: JID
    """
    new_jid = copy.deepcopy(jid)
    new_jid.RawAgent = 0
    new_jid.Device = 0
    return new_jid


def Jid2String(jid: JID) -> str:
    """Converts a Jabber Identifier (JID) to a string.

    :param jid: The Jabber Identifier (JID) to be converted.
    :type jid: JID
    :return: The string representation of the JID.
    :rtype: str
    """
    if jid.RawAgent > 0:
        return "%s.%s:%d@%s" % (jid.User, jid.RawAgent, jid.Device, jid.Server)
    elif jid.Device > 0:
        return "%s:%d@%s" % (jid.User, jid.Device, jid.Server)
    elif len(jid.User) > 0:
        return "%s@%s" % (jid.User, jid.Server)
    return jid.Server


def build_jid(phone_number: str, server: str = "s.whatsapp.net") -> JID:
    """
    Builds a JID (Jabber ID) from a phone number.

    :param phone_number: The phone number to be used for building the JID.
    :type phone_number: str
    :return: A JID object constructed from the given phone number.
    :rtype: JID
    """
    return JID(
        User=phone_number,
        Device=0,
        Integrator=0,
        IsEmpty=False,
        RawAgent=0,
        Server=server,
    )
