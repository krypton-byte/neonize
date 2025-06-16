import ctypes
import ctypes.util
import os
from platform import system
from typing import Any
from pathlib import Path
from .utils.platform import generated_name
from .download import download, __GONEONIZE_VERSION__

func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)  # qr
func = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_bool)  # blocking
func_bytes = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)  # status
func_callback_bytes = ctypes.CFUNCTYPE(
    None, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int
)  # callback_bytes


def load_goneonize():
    while True:
        try:
            gocode = ctypes.CDLL(f"{root_dir}/{generated_name()}")
            gocode.GetVersion.restype = ctypes.c_char_p
            if gocode.GetVersion().decode() != __GONEONIZE_VERSION__:
                raise Exception("Invalid Version")
            return gocode
        except OSError as e:
            print("e", e)
            raise e
        except Exception:
            download()


class Bytes(ctypes.Structure):
    ptr: int
    size: int
    _fields_ = [("ptr", ctypes.POINTER(ctypes.c_char)), ("size", ctypes.c_size_t)]

    def get_bytes(self):
        return ctypes.string_at(self.ptr, self.size)


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
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetLIDFromPN.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetLIDFromPN.restype = ctypes.POINTER(Bytes)
    gocode.GetPNFromLID.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetPNFromLID.restype = ctypes.POINTER(Bytes)
    gocode.Upload.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.TestStruct.argtypes = []
    gocode.TestStruct.restype = ctypes.POINTER(Bytes)
    gocode.Upload.restype = ctypes.POINTER(Bytes)
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
    gocode.LeaveGroup.restype = ctypes.c_char_p
    gocode.SetGroupName.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.SetGroupName.restype = ctypes.c_char_p
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
    gocode.SendChatPresence.restype = ctypes.c_char_p
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
    gocode.GenerateMessageID.restype = ctypes.c_char_p
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
    gocode.FollowNewsletter.restype = ctypes.c_char_p
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
    gocode.JoinGroupWithInvite.restype = ctypes.c_char_p
    gocode.LinkGroup.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.LinkGroup.restype = ctypes.POINTER(Bytes)
    gocode.Logout.argtypes = [ctypes.c_char_p]
    gocode.Logout.restype = ctypes.c_char_p
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
    gocode.MarkRead.restype = ctypes.c_char_p
    gocode.NewsletterMarkViewed.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.NewsletterMarkViewed.restype = ctypes.c_char_p
    gocode.NewsletterSendReaction.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.NewsletterSendReaction.restype = ctypes.c_char_p
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
    gocode.NewsletterToggleMute.restype = ctypes.c_char_p
    gocode.Disconnect.argtypes = [ctypes.c_char_p]
    gocode.ResolveContactQRLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.ResolveContactQRLink.restype = ctypes.POINTER(Bytes)
    gocode.ResolveBusinessMessageLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.ResolveBusinessMessageLink.restype = ctypes.POINTER(Bytes)
    gocode.SendAppState.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.SendAppState.restype = ctypes.c_char_p
    gocode.SetDefaultDisappearingTimer.argtypes = [ctypes.c_char_p, ctypes.c_int64]
    gocode.SetDefaultDisappearingTimer.restype = ctypes.c_char_p
    gocode.SetDisappearingTimer.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int64,
    ]
    gocode.SetDisappearingTimer.restype = ctypes.c_char_p
    gocode.SetForceActiveDeliveryReceipts.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    gocode.SetForceActiveDeliveryReceipts.restype = ctypes.c_void_p
    gocode.SetGroupAnnounce.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.SetGroupAnnounce.restype = ctypes.c_char_p
    gocode.SetGroupLocked.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.SetGroupLocked.restype = ctypes.c_char_p
    gocode.SetGroupTopic.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.SetGroupTopic.restype = ctypes.c_char_p
    gocode.SetPrivacySetting.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.SetPrivacySetting.restype = ctypes.POINTER(Bytes)
    gocode.SetPassive.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    gocode.SetPassive.restype = ctypes.c_char_p
    gocode.SetStatusMessage.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.SetStatusMessage.restype = ctypes.c_char_p
    gocode.SubscribePresence.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.SubscribePresence.restype = ctypes.c_char_p
    gocode.UnfollowNewsletter.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.UnfollowNewsletter.restype = ctypes.c_char_p
    gocode.UnlinkGroup.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.UnlinkGroup.restype = ctypes.c_char_p
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
    gocode.PutPushName.restype = ctypes.c_char_p
    gocode.PutAllContactNames.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.PutAllContactNames.restype = ctypes.c_char_p
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
    gocode.PutMutedUntil.restype = ctypes.c_char_p
    gocode.PutPinned.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.PutPinned.restype = ctypes.c_char_p
    gocode.PutArchived.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.PutArchived.restype = ctypes.c_char_p
    gocode.GetChatSettings.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetChatSettings.restype = ctypes.POINTER(Bytes)
    gocode.GetAllDevices.argtypes = [ctypes.c_char_p]
    gocode.GetAllDevices.restype = ctypes.c_char_p
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
    gocode.SendPresence.restype = ctypes.c_char_p
    gocode.DecryptPollVote.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.DecryptPollVote.restype = ctypes.POINTER(Bytes)
    gocode.Stop.argtypes = [ctypes.c_char_p]
    gocode.Stop.restype = ctypes.c_void_p
    gocode.StopAll.argtypes = []
    gocode.StopAll.restype = ctypes.c_void_p
    gocode.FreeBytesStruct.argtypes = [ctypes.POINTER(Bytes)]
    gocode.FreeBytesStruct.restype = None
else:
    gocode: Any = object()


def free_bytes(bytes_ptr: ctypes._Pointer):
    # print("Freeing bytes", bytes_ptr)
    gocode.FreeBytesStruct(bytes_ptr)
