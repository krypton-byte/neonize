import ctypes
import os

from platform import system

file_ext = "dll" if system() == "Windows" else "so"
root_dir = os.path.abspath(os.path.dirname(__file__))
gocode = ctypes.CDLL(f"{root_dir}/gocode/gocode.{file_ext}")
func_string = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
func_bytes = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
func_callback_bytes = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.c_int, ctypes.c_int
)


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
    func_string,
    func_string,
    func_callback_bytes,
    ctypes.c_char_p,
]
gocode.Upload.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
gocode.Upload.restype = Bytes
gocode.Download.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
gocode.Download.restype = Bytes
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
    ctypes.c_int
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
gocode.Logout.argtypes = [
    ctypes.c_char
]
gocode.Logout.restype = ctypes.c_char_p