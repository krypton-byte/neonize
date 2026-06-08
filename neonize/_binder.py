import ctypes
import ctypes.util
import os
from dataclasses import dataclass
from pathlib import Path
from platform import system
from typing import Any, Optional

from .download import __GONEONIZE_VERSION__, download
from .utils.platform import generated_name

func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)  # qr
func = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool)  # blocking
func_bytes = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)  # status
func_callback_bytes = ctypes.CFUNCTYPE(
    None, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int
)  # callback_bytes

func_callback_bytes2 = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)  # callback_bytes


def load_goneonize():
    last_error: Exception | None = None
    for _ in range(3):
        try:
            gocode = ctypes.CDLL(f"{root_dir}/{generated_name()}")
            gocode.GetVersion.restype = ctypes.c_char_p
            if gocode.GetVersion().decode() != __GONEONIZE_VERSION__:
                raise Exception("Invalid Version")
            return gocode
        except OSError as e:
            print("e", e)
            raise e
        except Exception as e:
            last_error = e
            download()
    raise RuntimeError(
        f"failed to load goneonize after 3 attempts; last error: {last_error}"
    )


class Bytes(ctypes.Structure):
    _fields_ = [("ptr", ctypes.c_char_p), ("size", ctypes.c_size_t)]

    def get_bytes(self):
        return ctypes.string_at(self.ptr, self.size)


class _CProxySettings(ctypes.Structure):
    """Internal ctypes struct that mirrors C.struct_ProxySettings in cstruct.h.
    Do not use directly — use :class:`ProxySettings` dataclass instead.
    """

    _fields_ = [
        ("proxyAddress", ctypes.c_char_p),
        ("noWebsocket", ctypes.c_bool),
        ("onlyLogin", ctypes.c_bool),
        ("noMedia", ctypes.c_bool),
    ]


@dataclass
class ProxySettings:
    """Proxy configuration for the WhatsApp client.

    Example::

        # Connect with a SOCKS5 proxy
        proxy = ProxySettings(proxy_address="socks5://127.0.0.1:1080")
        client.connect(proxy)

        # Proxy only during login, skip media traffic
        proxy = ProxySettings(
            proxy_address="http://proxy.example.com:8080",
            only_login=True,
            no_media=True,
        )
        client.connect(proxy)
    """

    proxy_address: str
    """Proxy URL, e.g. ``socks5://host:port`` or ``http://host:port``."""

    no_websocket: bool = False
    """If True, don't route WebSocket traffic through the proxy."""

    only_login: bool = False
    """If True, only use the proxy during the login/pairing phase."""

    no_media: bool = False
    """If True, don't route media uploads/downloads through the proxy."""

    def _to_c_struct(self) -> "_CProxySettings":
        """Convert this dataclass into the internal ctypes struct for CGO."""
        return _CProxySettings(
            proxyAddress=self.proxy_address.encode(),
            noWebsocket=self.no_websocket,
            onlyLogin=self.only_login,
            noMedia=self.no_media,
        )


if not os.environ.get("SPHINX"):
    if not (Path(__file__).parent / generated_name()).exists():
        download()
    file_ext = "dll" if system() == "Windows" else "so"
    root_dir = os.path.abspath(os.path.dirname(__file__))
    gocode = load_goneonize()

    gocode.Neonize.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        func_string,
        func_string,
        func_callback_bytes,
        func_callback_bytes2,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.POINTER(_CProxySettings),
    ]
    gocode.Neonize.restype = ctypes.c_void_p
    gocode.GetLIDFromPN.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetLIDFromPN.restype = ctypes.POINTER(Bytes)
    gocode.GetPNFromLID.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetPNFromLID.restype = ctypes.POINTER(Bytes)
    gocode.PinMessage.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.PinMessage.restype = ctypes.POINTER(Bytes)
    gocode.Upload.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.TestStruct.argtypes = []
    gocode.TestStruct.restype = ctypes.POINTER(Bytes)
    gocode.Upload.restype = ctypes.POINTER(Bytes)
    gocode.UploadNewsletter.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.UploadNewsletter.restype = ctypes.POINTER(Bytes)
    gocode.DownloadAny.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.DownloadAny.restype = ctypes.POINTER(Bytes)
    gocode.DownloadMediaWithPath.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.DownloadMediaWithPath.restype = ctypes.POINTER(Bytes)
    gocode.GetGroupInfo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetGroupInfo.restype = ctypes.POINTER(Bytes)
    gocode.SetGroupPhoto.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.SetGroupPhoto.restype = ctypes.POINTER(Bytes)
    gocode.SetProfilePhoto.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.SetProfilePhoto.restype = ctypes.POINTER(Bytes)
    gocode.LeaveGroup.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.LeaveGroup.restype = ctypes.c_void_p
    gocode.SetGroupName.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.SetGroupName.restype = ctypes.c_void_p
    gocode.GetGroupInviteLink.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.GetGroupInviteLink.restype = ctypes.POINTER(Bytes)
    gocode.JoinGroupWithLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.JoinGroupWithLink.restype = ctypes.POINTER(Bytes)
    gocode.SendMessage.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.SendMessage.restype = ctypes.POINTER(Bytes)
    gocode.SendChatPresence.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.SendChatPresence.restype = ctypes.c_void_p
    gocode.BuildRevoke.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.BuildRevoke.restype = ctypes.POINTER(Bytes)
    gocode.CreateGroup.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.CreateGroup.restype = ctypes.POINTER(Bytes)
    gocode.GenerateMessageID.argtypes = [ctypes.c_char_p]
    gocode.GenerateMessageID.restype = ctypes.c_void_p
    gocode.IsOnWhatsApp.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.IsOnWhatsApp.restype = ctypes.POINTER(Bytes)
    gocode.IsConnected.argtypes = [ctypes.c_char_p]
    gocode.IsConnected.restype = ctypes.c_bool
    gocode.IsLoggedIn.argtypes = [ctypes.c_char_p]
    gocode.IsLoggedIn.restype = ctypes.c_bool
    gocode.GetUserInfo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetUserInfo.restype = ctypes.POINTER(Bytes)
    gocode.GetMe.argtypes = [ctypes.c_char_p]
    gocode.GetMe.restype = ctypes.POINTER(Bytes)
    gocode.BuildPollVoteCreation.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.BuildPollVoteCreation.restype = ctypes.POINTER(Bytes)
    gocode.BuildPollVote.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.BuildPollVote.restype = ctypes.POINTER(Bytes)
    gocode.BuildReaction.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.BuildReaction.restype = ctypes.POINTER(Bytes)
    gocode.CreateNewsletter.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.CreateNewsletter.restype = ctypes.POINTER(Bytes)
    gocode.FollowNewsletter.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.FollowNewsletter.restype = ctypes.c_void_p
    gocode.GetBlocklist.argtypes = [ctypes.c_char_p]
    gocode.GetBlocklist.restype = ctypes.POINTER(Bytes)
    gocode.GetContactQRLink.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    gocode.GetContactQRLink.restype = ctypes.POINTER(Bytes)
    gocode.GetGroupInfoFromInvite.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetGroupInfoFromInvite.restype = ctypes.POINTER(Bytes)
    gocode.GetGroupInfoFromLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.GetGroupInfoFromLink.restype = ctypes.POINTER(Bytes)
    gocode.GetGroupRequestParticipants.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetGroupRequestParticipants.restype = ctypes.POINTER(Bytes)
    gocode.GetJoinedGroups.argtypes = [ctypes.c_char_p]
    gocode.GetJoinedGroups.restype = ctypes.POINTER(Bytes)
    gocode.GetLinkedGroupsParticipants.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetLinkedGroupsParticipants.restype = ctypes.POINTER(Bytes)
    gocode.GetNewsletterInfo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetNewsletterInfo.restype = ctypes.POINTER(Bytes)
    gocode.GetNewsletterInfoWithInvite.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.GetNewsletterInfoWithInvite.restype = ctypes.POINTER(Bytes)
    gocode.GetNewsletterMessageUpdate.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.GetNewsletterMessageUpdate.restype = ctypes.POINTER(Bytes)
    gocode.GetNewsletterMessages.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.GetNewsletterMessages.restype = ctypes.POINTER(Bytes)
    gocode.GetPrivacySettings.argtypes = [ctypes.c_char_p]
    gocode.GetPrivacySettings.restype = ctypes.POINTER(Bytes)
    gocode.GetProfilePicture.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetProfilePicture.restype = ctypes.POINTER(Bytes)
    gocode.GetStatusPrivacy.argtypes = [ctypes.c_char_p]
    gocode.GetStatusPrivacy.restype = ctypes.POINTER(Bytes)
    gocode.GetSubGroups.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetSubGroups.restype = ctypes.POINTER(Bytes)
    gocode.GetSubscribedNewsletters.argtypes = [ctypes.c_char_p]
    gocode.GetSubscribedNewsletters.restype = ctypes.POINTER(Bytes)
    gocode.GetUserDevices.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetUserDevices.restype = ctypes.POINTER(Bytes)
    gocode.JoinGroupWithInvite.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.JoinGroupWithInvite.restype = ctypes.c_void_p
    gocode.LinkGroup.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.LinkGroup.restype = ctypes.c_void_p
    gocode.Logout.argtypes = [ctypes.c_char_p]
    gocode.Logout.restype = ctypes.c_void_p
    gocode.MarkRead.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.MarkRead.restype = ctypes.c_void_p
    gocode.NewsletterMarkViewed.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.NewsletterMarkViewed.restype = ctypes.c_void_p
    gocode.NewsletterSendReaction.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.NewsletterSendReaction.restype = ctypes.c_void_p
    gocode.NewsletterSubscribeLiveUpdates.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.NewsletterSubscribeLiveUpdates.restype = ctypes.POINTER(Bytes)
    gocode.NewsletterToggleMute.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.NewsletterToggleMute.restype = ctypes.c_void_p
    gocode.Disconnect.argtypes = [ctypes.c_char_p]
    gocode.ResolveContactQRLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.ResolveContactQRLink.restype = ctypes.POINTER(Bytes)
    gocode.ResolveBusinessMessageLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.ResolveBusinessMessageLink.restype = ctypes.POINTER(Bytes)
    gocode.PairPhone.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.PairPhone.restype = ctypes.POINTER(Bytes)
    gocode.SendAppState.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.SendAppState.restype = ctypes.c_void_p
    gocode.SetDefaultDisappearingTimer.argtypes = [ctypes.c_char_p, ctypes.c_int64]
    gocode.SetDefaultDisappearingTimer.restype = ctypes.c_void_p
    gocode.SetDisappearingTimer.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int64,
        ctypes.c_int64,
    ]
    gocode.SetDisappearingTimer.restype = ctypes.c_void_p
    gocode.SetForceActiveDeliveryReceipts.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    gocode.SetForceActiveDeliveryReceipts.restype = ctypes.c_void_p
    gocode.SetGroupAnnounce.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.SetGroupAnnounce.restype = ctypes.c_void_p
    gocode.SetGroupLocked.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.SetGroupLocked.restype = ctypes.c_void_p
    gocode.SetGroupTopic.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.SetGroupTopic.restype = ctypes.c_void_p
    gocode.SetPrivacySetting.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.SetPrivacySetting.restype = ctypes.POINTER(Bytes)
    gocode.SetPassive.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    gocode.SetPassive.restype = ctypes.c_void_p
    gocode.SetStatusMessage.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.SetStatusMessage.restype = ctypes.c_void_p
    gocode.SubscribePresence.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.SubscribePresence.restype = ctypes.c_void_p
    gocode.UnfollowNewsletter.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.UnfollowNewsletter.restype = ctypes.c_void_p
    gocode.UnlinkGroup.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.UnlinkGroup.restype = ctypes.c_void_p
    gocode.UpdateBlocklist.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.UpdateBlocklist.restype = ctypes.POINTER(Bytes)
    gocode.UpdateGroupParticipants.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.UpdateGroupParticipants.restype = ctypes.POINTER(Bytes)
    gocode.GetMessageForRetry.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.GetMessageForRetry.restype = ctypes.POINTER(Bytes)
    gocode.PutPushName.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.PutPushName.restype = ctypes.POINTER(Bytes)
    gocode.PutContactName.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.PutContactName.restype = ctypes.c_void_p
    gocode.PutAllContactNames.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.PutAllContactNames.restype = ctypes.c_void_p
    gocode.GetContact.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetContact.restype = ctypes.POINTER(Bytes)
    gocode.GetAllContacts.argtypes = [ctypes.c_char_p]
    gocode.GetAllContacts.restype = ctypes.POINTER(Bytes)
    gocode.PutMutedUntil.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_float,
    ]
    gocode.PutMutedUntil.restype = ctypes.c_void_p
    gocode.PutPinned.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.PutPinned.restype = ctypes.c_void_p
    gocode.PutArchived.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.PutArchived.restype = ctypes.c_void_p
    gocode.GetChatSettings.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetChatSettings.restype = ctypes.POINTER(Bytes)
    gocode.GetAllDevices.argtypes = [ctypes.c_char_p, func_callback_bytes2]
    gocode.GetAllDevices.restype = ctypes.c_void_p
    gocode.SendFBMessage.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.SendFBMessage.restype = ctypes.POINTER(Bytes)
    gocode.SendPresence.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.SendPresence.restype = ctypes.c_void_p
    gocode.DecryptPollVote.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.DecryptPollVote.restype = ctypes.POINTER(Bytes)
    gocode.Stop.argtypes = [ctypes.c_char_p]
    gocode.Stop.restype = ctypes.c_void_p
    gocode.StopAll.argtypes = []
    gocode.StopAll.restype = ctypes.c_void_p
    gocode.FreeBytesStruct.argtypes = [ctypes.POINTER(Bytes)]
    gocode.FreeBytesStruct.restype = None
    gocode.SetPushName.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.SetPushName.restype = ctypes.c_void_p
    gocode.SetPushName.errcheck = consume_cstring
    gocode.SetProxyAddress.argtypes = [ctypes.c_char_p, ctypes.POINTER(_CProxySettings)]
    gocode.SetProxyAddress.restype = ctypes.c_void_p
    gocode.SetProxyAddress.errcheck = consume_cstring

    gocode.FreeString.argtypes = [ctypes.c_void_p]
    gocode.FreeString.restype = None

    def consume_cstring(result, func, arguments):
        """ctypes errcheck for FFI functions returning a Go-allocated ``*C.char``.

        Copies the string into ``bytes`` -- exactly what a ``c_char_p`` restype
        used to yield, so callers are unaffected -- then frees the C allocation
        via ``FreeString``. Without this the Go ``C.CString`` is leaked on every
        call: a ``c_char_p`` restype copies the bytes and discards the pointer,
        leaving the allocation unreachable.
        """
        if not result:
            return b""
        try:
            return ctypes.string_at(result)
        finally:
            gocode.FreeString(result)

    # FFI functions that return a Go-allocated C string. Each is declared
    # ``restype = ctypes.c_void_p`` above so the raw pointer survives the call;
    # ``consume_cstring`` then reads and frees it. Keep this list in sync with
    # those declarations. (GetVersion is intentionally excluded: it is called
    # once during bootstrap, so its one-off leak is negligible and freeing it
    # is kept out of the binary-loading path.)
    for _string_returning_func in (
        "Neonize",
        "LeaveGroup",
        "SetGroupName",
        "SendChatPresence",
        "GenerateMessageID",
        "FollowNewsletter",
        "JoinGroupWithInvite",
        "LinkGroup",
        "Logout",
        "MarkRead",
        "NewsletterMarkViewed",
        "NewsletterSendReaction",
        "NewsletterToggleMute",
        "SendAppState",
        "SetDefaultDisappearingTimer",
        "SetDisappearingTimer",
        "SetGroupAnnounce",
        "SetGroupLocked",
        "SetGroupTopic",
        "SetPassive",
        "SetStatusMessage",
        "SubscribePresence",
        "UnfollowNewsletter",
        "UnlinkGroup",
        "PutContactName",
        "PutAllContactNames",
        "PutMutedUntil",
        "PutPinned",
        "PutArchived",
        "GetAllDevices",
        "SendPresence",
        "SetPushName",
    ):
        getattr(gocode, _string_returning_func).errcheck = consume_cstring
else:
    gocode: Any = object()


def free_bytes(bytes_ptr: ctypes._Pointer):
    # print("Freeing bytes", bytes_ptr)
    gocode.FreeBytesStruct(bytes_ptr)
