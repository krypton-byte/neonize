import ctypes
import os
from platform import system
import importlib.metadata
from typing import Any
from pathlib import Path

func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
func = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
func_bytes = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
func_callback_bytes = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.c_int, ctypes.c_int
)
from .utils.platform import generated_name
from .download import download


def load_goneonize():
    while True:
        try:
            gocode = ctypes.CDLL(f"{root_dir}/{generated_name()}")
            gocode.GetVersion.restype = ctypes.c_char_p
            if gocode.GetVersion().decode() != importlib.metadata.version("neonize"):
                download()
                raise Exception("Unmatched version")
            return gocode
        except OSError as e:
            raise e
        except Exception:
            download()


if not os.environ.get("SPHINX"):
    if not (Path(__file__).parent / generated_name()).exists():
        download()
    file_ext = "dll" if system() == "Windows" else "so"
    root_dir = os.path.abspath(os.path.dirname(__file__))
    gocode = load_goneonize()

    class Bytes(ctypes.Structure):
        ptr: int
        size: int
        _fields_ = [("ptr", ctypes.POINTER(ctypes.c_char)), ("size", ctypes.c_size_t)]

        def get_bytes(self):
            return ctypes.string_at(self.ptr, self.size)

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
        func,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.Upload.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.Upload.restype = Bytes
    gocode.DownloadAny.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.DownloadAny.restype = Bytes
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
    gocode.DownloadMediaWithPath.restype = Bytes
    gocode.GetGroupInfo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetGroupInfo.restype = Bytes
    gocode.SetGroupPhoto.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.SetGroupPhoto.restype = ctypes.c_char_p
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
    gocode.GetGroupInviteLink.restype = Bytes
    gocode.JoinGroupWithLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.JoinGroupWithLink.restype = Bytes
    gocode.SendMessage.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.SendMessage.restype = Bytes
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
    gocode.BuildRevoke.restype = Bytes
    gocode.CreateGroup.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.CreateGroup.restype = Bytes
    gocode.GenerateMessageID.argtypes = [ctypes.c_char_p]
    gocode.GenerateMessageID.restype = ctypes.c_char_p
    gocode.IsOnWhatsApp.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.IsOnWhatsApp.restype = Bytes
    gocode.IsConnected.argtypes = [ctypes.c_char_p]
    gocode.IsConnected.restype = ctypes.c_bool
    gocode.IsLoggedIn.argtypes = [ctypes.c_char_p]
    gocode.IsLoggedIn.restype = ctypes.c_bool
    gocode.GetUserInfo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetUserInfo.restype = Bytes
    gocode.GetMe.argtypes = [ctypes.c_char_p]
    gocode.GetMe.restype = Bytes
    gocode.BuildPollVoteCreation.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.BuildPollVoteCreation.restype = Bytes
    gocode.BuildPollVote.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.BuildPollVote.restype = Bytes
    gocode.BuildReaction.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    gocode.BuildReaction.restype = Bytes
    gocode.CreateNewsletter.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.CreateNewsletter.restype = Bytes
    gocode.FollowNewsletter.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.FollowNewsletter.restype = ctypes.c_char_p
    gocode.GetBlocklist.argtypes = [ctypes.c_char_p]
    gocode.GetBlocklist.restype = Bytes
    gocode.GetContactQRLink.argtypes = [ctypes.c_char_p, ctypes.c_bool]
    gocode.GetContactQRLink.restype = Bytes
    gocode.GetGroupInfoFromInvite.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetGroupInfoFromInvite.restype = Bytes
    gocode.GetGroupInfoFromLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.GetGroupInfoFromLink.restype = Bytes
    gocode.GetGroupRequestParticipants.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetGroupRequestParticipants.restype = Bytes
    gocode.GetJoinedGroups.argtypes = [ctypes.c_char_p]
    gocode.GetJoinedGroups.restype = Bytes
    gocode.GetLinkedGroupsParticipants.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetLinkedGroupsParticipants.restype = Bytes
    gocode.GetNewsletterInfo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetNewsletterInfo.restype = Bytes
    gocode.GetNewsletterInfoWithInvite.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.GetNewsletterInfoWithInvite.restype = Bytes
    gocode.GetNewsletterMessageUpdate.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.GetNewsletterMessageUpdate.restype = Bytes
    gocode.GetNewsletterMessages.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    gocode.GetNewsletterMessages.restype = Bytes
    gocode.GetPrivacySettings.argtypes = [ctypes.c_char_p]
    gocode.GetPrivacySettings.restype = Bytes
    gocode.GetProfilePicture.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    gocode.GetProfilePicture.restype = Bytes
    gocode.GetStatusPrivacy.argtypes = [ctypes.c_char_p]
    gocode.GetStatusPrivacy.restype = Bytes
    gocode.GetSubGroups.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetSubGroups.restype = Bytes
    gocode.GetSubscribedNewsletters.argtypes = [ctypes.c_char_p]
    gocode.GetSubscribedNewsletters.restype = Bytes
    gocode.GetUserDevices.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    gocode.GetUserDevices.restype = Bytes
    gocode.JoinGroupWithLink.argtypes = [
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
    gocode.LinkGroup.restype = Bytes
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
    gocode.NewsletterSubscribeLiveUpdates.restype = Bytes
    gocode.NewsletterToggleMute.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_bool,
    ]
    gocode.NewsletterToggleMute.restype = ctypes.c_char_p
    gocode.Disconnect.argtypes = [ctypes.c_char_p]
    gocode.ResolveContactQRLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.ResolveContactQRLink.restype = Bytes
    gocode.ResolveBusinessMessageLink.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    gocode.ResolveBusinessMessageLink.restype = Bytes
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
    gocode.SetPrivacySetting.restype = Bytes
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
    gocode.UpdateBlocklist.restype = Bytes
    gocode.UpdateGroupParticipants.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.UpdateGroupParticipants.restype = Bytes
    gocode.GetMessageForRetry.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.GetMessageForRetry.restype = Bytes
    gocode.PutPushName.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
    ]
    gocode.PutPushName.restype = Bytes
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
    gocode.GetContact.restype = Bytes
    gocode.GetAllContacts.argtypes = [ctypes.c_char_p]
    gocode.GetAllContacts.restype = Bytes
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
    gocode.GetChatSettings.restype = Bytes
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
    gocode.SendFBMessage.restype = Bytes
else:
    gocode: Any = object()
