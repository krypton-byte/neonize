from neonize.aioze.events import RotateADVSecretEv as AioRotateADVSecretEv
from neonize.events import EVENT_TO_INT, INT_TO_EVENT, RotateADVSecretEv
from neonize.proto.Neonize_pb2 import JID, MessageDebugTimings, RotateADVSecret, SendResponse


def test_send_response_has_sender_and_chat():
    sender = JID(
        User="1234567890",
        RawAgent=0,
        Device=0,
        Integrator=0,
        Server="s.whatsapp.net",
    )
    chat = JID(
        User="9876543210",
        RawAgent=0,
        Device=0,
        Integrator=0,
        Server="s.whatsapp.net",
    )
    timings = MessageDebugTimings(
        Queue=0,
        Marshal=0,
        GetParticipants=0,
        GetDevices=0,
        GroupEncrypt=0,
        PeerEncrypt=0,
        Send=0,
        Resp=0,
        Retry=0,
    )
    resp = SendResponse(
        Timestamp=1700000000,
        ID="ABCDEF123456",
        ServerID=12345,
        DebugTimings=timings,
        Sender=sender,
        Chat=chat,
    )
    serialized = resp.SerializeToString()
    deserialized = SendResponse.FromString(serialized)

    assert deserialized.ID == "ABCDEF123456"
    assert deserialized.Sender.User == "1234567890"
    assert deserialized.Chat.User == "9876543210"


def test_rotate_adv_secret_event():
    assert EVENT_TO_INT[RotateADVSecretEv] == 45
    assert INT_TO_EVENT[45] is RotateADVSecretEv
    assert AioRotateADVSecretEv is RotateADVSecretEv

    rot = RotateADVSecret(OldSecret="old_sec_key", NewSecret="new_sec_key")
    data = rot.SerializeToString()
    parsed = RotateADVSecret.FromString(data)
    assert parsed.OldSecret == "old_sec_key"
    assert parsed.NewSecret == "new_sec_key"


def test_pair_phone_without_connect_raises_clean_error(tmp_path):
    import os

    import pytest

    if os.environ.get("SPHINX"):
        pytest.skip("Skipping live CGO call in SPHINX mock mode")

    from neonize.client import NewClient
    from neonize.exc import PairPhoneError

    db_path = str(tmp_path / "session.db")
    c = NewClient(db_path)
    with pytest.raises(PairPhoneError, match="client is nil"):
        c.PairPhone("1234567890", True)


def test_chat_state_events_are_registered():
    from neonize.aioze import events as aio_events
    from neonize.events import ChatArchiveEv, ChatMarkAsReadEv, ChatMuteEv, ChatPinEv
    from neonize.proto.Neonize_pb2 import ChatArchive
    from neonize.proto.waSyncAction.WAWebProtobufSyncAction_pb2 import ArchiveChatAction

    for code, name, ev in (
        (46, "ChatArchiveEv", ChatArchiveEv),
        (47, "ChatPinEv", ChatPinEv),
        (48, "ChatMuteEv", ChatMuteEv),
        (49, "ChatMarkAsReadEv", ChatMarkAsReadEv),
    ):
        assert EVENT_TO_INT[ev] == code
        assert INT_TO_EVENT[code] is ev
        assert name in aio_events.__all__ and getattr(aio_events, name) is ev

    chat = JID(User="5551", RawAgent=0, Device=0, Integrator=0, Server="s.whatsapp.net")
    evt = ChatArchive(
        JID=chat, Timestamp=1792000000, FromFullSync=False, Action=ArchiveChatAction(archived=True)
    )
    parsed = ChatArchive.FromString(evt.SerializeToString())
    assert parsed.JID.User == "5551" and parsed.Action.archived is True


def test_chat_delete_event_is_registered():
    from neonize.aioze import events as aio_events
    from neonize.events import ChatDeleteEv
    from neonize.proto.Neonize_pb2 import ChatDelete
    from neonize.proto.waSyncAction.WAWebProtobufSyncAction_pb2 import DeleteChatAction

    assert EVENT_TO_INT[ChatDeleteEv] == 51
    assert INT_TO_EVENT[51] is ChatDeleteEv
    assert "ChatDeleteEv" in aio_events.__all__ and aio_events.ChatDeleteEv is ChatDeleteEv

    chat = JID(User="5551", RawAgent=0, Device=0, Integrator=0, Server="s.whatsapp.net")
    evt = ChatDelete(
        JID=chat,
        Timestamp=1792000000,
        FromFullSync=False,
        DeleteMedia=True,
        Action=DeleteChatAction(),
    )
    parsed = ChatDelete.FromString(evt.SerializeToString())
    assert parsed.JID.User == "5551" and parsed.Timestamp == 1792000000 and parsed.DeleteMedia


def test_message_delete_for_me_event_is_registered():
    from neonize.aioze import events as aio_events
    from neonize.events import MessageDeleteForMeEv
    from neonize.proto.Neonize_pb2 import MessageDeleteForMe
    from neonize.proto.waSyncAction.WAWebProtobufSyncAction_pb2 import (
        DeleteMessageForMeAction,
    )

    assert EVENT_TO_INT[MessageDeleteForMeEv] == 52
    assert INT_TO_EVENT[52] is MessageDeleteForMeEv
    assert "MessageDeleteForMeEv" in aio_events.__all__
    assert aio_events.MessageDeleteForMeEv is MessageDeleteForMeEv

    chat = JID(User="5551", RawAgent=0, Device=0, Integrator=0, Server="s.whatsapp.net")
    evt = MessageDeleteForMe(
        ChatJID=chat,
        IsFromMe=True,
        MessageID="3EB0ABC",
        Timestamp=1792000000,
        FromFullSync=False,
        Action=DeleteMessageForMeAction(deleteMedia=True),
    )
    parsed = MessageDeleteForMe.FromString(evt.SerializeToString())
    assert parsed.ChatJID.User == "5551" and parsed.MessageID == "3EB0ABC"
    assert parsed.IsFromMe and parsed.Action.deleteMedia


def test_message_star_event_is_registered():
    from neonize.aioze import events as aio_events
    from neonize.events import MessageStarEv
    from neonize.proto.Neonize_pb2 import MessageStar
    from neonize.proto.waSyncAction.WAWebProtobufSyncAction_pb2 import StarAction

    assert EVENT_TO_INT[MessageStarEv] == 53
    assert INT_TO_EVENT[53] is MessageStarEv
    assert "MessageStarEv" in aio_events.__all__
    assert aio_events.MessageStarEv is MessageStarEv

    chat = JID(User="5551", RawAgent=0, Device=0, Integrator=0, Server="s.whatsapp.net")
    evt = MessageStar(
        ChatJID=chat,
        IsFromMe=True,
        MessageID="3EB0ABC",
        Timestamp=1792000000,
        FromFullSync=False,
        Action=StarAction(starred=True),
    )
    parsed = MessageStar.FromString(evt.SerializeToString())
    assert parsed.ChatJID.User == "5551" and parsed.MessageID == "3EB0ABC"
    assert parsed.IsFromMe and parsed.Action.starred


def test_chat_clear_event_is_registered():
    from neonize.aioze import events as aio_events
    from neonize.events import ChatClearEv
    from neonize.proto.Neonize_pb2 import ChatClear
    from neonize.proto.waSyncAction.WAWebProtobufSyncAction_pb2 import (
        ClearChatAction,
    )

    assert EVENT_TO_INT[ChatClearEv] == 54
    assert INT_TO_EVENT[54] is ChatClearEv
    assert "ChatClearEv" in aio_events.__all__
    assert aio_events.ChatClearEv is ChatClearEv

    chat = JID(User="5551", RawAgent=0, Device=0, Integrator=0, Server="s.whatsapp.net")
    evt = ChatClear(
        JID=chat,
        Timestamp=1792000000,
        FromFullSync=False,
        DeleteMedia=True,
        Action=ClearChatAction(),
    )
    parsed = ChatClear.FromString(evt.SerializeToString())
    assert parsed.JID.User == "5551" and parsed.Timestamp == 1792000000
    assert parsed.DeleteMedia and not parsed.FromFullSync


def test_app_state_repair_methods_exist():
    import inspect

    from neonize.aioze.client import NewAClient
    from neonize.client import NewClient

    for cls in (NewClient, NewAClient):
        assert list(inspect.signature(cls.fetch_app_state).parameters) == [
            "self",
            "name",
            "full_sync",
        ]
        assert list(inspect.signature(cls.request_app_state_recovery).parameters) == [
            "self",
            "name",
        ]


def test_get_business_profile_methods_exist():
    import inspect

    from neonize.aioze.client import NewAClient
    from neonize.client import NewClient

    for cls in (NewClient, NewAClient):
        assert list(inspect.signature(cls.get_business_profile).parameters) == [
            "self",
            "jid",
        ]


def test_group_join_and_member_add_methods_exist():
    import inspect
    from unittest.mock import MagicMock

    from neonize.aioze.client import NewAClient
    from neonize.client import NewClient
    from neonize.exc import (
        SetGroupJoinApprovalModeError,
        SetGroupMemberAddModeError,
        UpdateGroupRequestParticipantsError,
    )
    from neonize.proto.Neonize_pb2 import GroupParticipant, UpdateGroupParticipantsReturnFunction
    from neonize.utils.enum import GroupMemberAddMode, ParticipantRequestChange

    assert GroupMemberAddMode.ADMIN_ADD.value == "admin_add"
    assert GroupMemberAddMode.ALL_MEMBER_ADD.value == "all_member_add"
    assert ParticipantRequestChange.APPROVE.value == "approve"
    assert ParticipantRequestChange.REJECT.value == "reject"

    for cls in (NewClient, NewAClient):
        assert list(inspect.signature(cls.set_group_join_approval_mode).parameters) == [
            "self",
            "jid",
            "mode",
        ]
        assert list(inspect.signature(cls.set_group_member_add_mode).parameters) == [
            "self",
            "jid",
            "mode",
        ]
        assert list(inspect.signature(cls.update_group_request_participants).parameters) == [
            "self",
            "jid",
            "participants",
            "action",
        ]

    def make_jid(user: str, server: str = "s.whatsapp.net") -> JID:
        return JID(User=user, RawAgent=0, Device=0, Integrator=0, Server=server)

    part_jid = make_jid("12345")
    mock_ret = UpdateGroupParticipantsReturnFunction(
        participants=[
            GroupParticipant(
                JID=part_jid,
                LID=part_jid,
                PhoneNumber=part_jid,
                IsAdmin=False,
                IsSuperAdmin=False,
                DisplayName="",
                Error=0,
            )
        ]
    ).SerializeToString()

    client = NewClient.__new__(NewClient)
    client.uuid = b"test-uuid"
    mock_binder = MagicMock()
    mock_binder.UpdateGroupRequestParticipants.return_value = mock_ret
    client._NewClient__client = mock_binder

    group_jid = make_jid("group123", "g.us")
    res = client.update_group_request_participants(
        group_jid, [part_jid], ParticipantRequestChange.APPROVE
    )
    assert len(res) == 1
    assert res[0].JID.User == "12345"

    # Test error raising
    import pytest

    mock_err_ret = UpdateGroupParticipantsReturnFunction(Error="request failed").SerializeToString()
    mock_binder.UpdateGroupRequestParticipants.return_value = mock_err_ret
    with pytest.raises(UpdateGroupRequestParticipantsError, match="request failed"):
        client.update_group_request_participants(
            group_jid, [part_jid], ParticipantRequestChange.REJECT
        )

    mock_binder.SetGroupJoinApprovalMode.return_value = b"approval error"
    with pytest.raises(SetGroupJoinApprovalModeError, match="approval error"):
        client.set_group_join_approval_mode(group_jid, True)

    mock_binder.SetGroupMemberAddMode.return_value = b"member add error"
    with pytest.raises(SetGroupMemberAddModeError, match="member add error"):
        client.set_group_member_add_mode(group_jid, GroupMemberAddMode.ADMIN_ADD)

    import asyncio

    async def _test_async():
        aclient = NewAClient.__new__(NewAClient)
        aclient.uuid = b"test-uuid"
        mock_abinder = MagicMock()

        async def _mock_update(*args, **kwargs):
            return mock_ret

        async def _mock_join_mode(*args, **kwargs):
            return b""

        async def _mock_member_mode(*args, **kwargs):
            return b""

        mock_abinder.UpdateGroupRequestParticipants = _mock_update
        mock_abinder.SetGroupJoinApprovalMode = _mock_join_mode
        mock_abinder.SetGroupMemberAddMode = _mock_member_mode
        aclient._NewAClient__client = mock_abinder

        ares = await aclient.update_group_request_participants(
            group_jid, [part_jid], ParticipantRequestChange.APPROVE
        )
        assert len(ares) == 1
        assert ares[0].JID.User == "12345"
        await aclient.set_group_join_approval_mode(group_jid, False)
        await aclient.set_group_member_add_mode(group_jid, GroupMemberAddMode.ALL_MEMBER_ADD)

    asyncio.run(_test_async())
