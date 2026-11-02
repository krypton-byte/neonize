"""Exception hierarchy for the neonize library.

All neonize-specific exceptions inherit from :class:`NeonizeError`, so
callers can write a single ``except NeonizeError`` to catch any library
error.

The hierarchy is organized by domain:

- **Transport** -- upload, download, proxy, connection.
- **Messaging** -- send, build, react, poll.
- **Group** -- create, join, leave, invite, settings.
- **Newsletter** -- follow, subscribe, reactions, mute.
- **Contact** -- store, profile, presence.
- **Chat Settings** -- mute, pin, archive.
- **Media** -- sticker conversion, FFmpeg.

Users who need finer-grained handling can catch the specific subclass;
everyone else can rely on the common base.
"""

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------


class NeonizeError(Exception):
    """Base class for all neonize-specific errors.

    Catch this to handle any error originating from the neonize library
    without enumerating every individual exception type.
    """


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------


class UploadError(NeonizeError):
    """Raised when media upload to WhatsApp servers fails."""


class DownloadError(NeonizeError):
    """Raised when media download from WhatsApp servers fails."""


# ---------------------------------------------------------------------------
# Messaging
# ---------------------------------------------------------------------------


class SendMessageError(NeonizeError):
    """Raised when sending a message fails."""


class BuildPollVoteError(NeonizeError):
    """Raised when building a poll vote message fails."""


class BuildPollVoteCreationError(NeonizeError):
    """Raised when building a poll creation message fails."""


class DecryptPollVoteError(NeonizeError):
    """Raised when decrypting a poll vote fails."""


# ---------------------------------------------------------------------------
# Group
# ---------------------------------------------------------------------------


class CreateGroupError(NeonizeError):
    """Raised when creating a WhatsApp group fails."""


class GetGroupInfoError(NeonizeError):
    """Raised when retrieving group information fails."""


class GetGroupInviteLinkError(NeonizeError):
    """Raised when retrieving a group invite link fails."""


class GetJoinedGroupsError(NeonizeError):
    """Raised when listing joined groups fails."""


class GetLinkedGroupParticipantsError(NeonizeError):
    """Raised when retrieving linked group participants fails."""


class GetGroupRequestParticipantsError(NeonizeError):
    """Raised when retrieving group join-request participants fails."""


class GetSubGroupsError(NeonizeError):
    """Raised when retrieving sub-groups fails."""


class JoinGroupWithInviteError(NeonizeError):
    """Raised when joining a group via invite link fails."""


class InviteLinkError(NeonizeError):
    """Raised when processing an invite link fails."""


class LinkGroupError(NeonizeError):
    """Raised when linking parent/child groups fails."""


class UnlinkGroupError(NeonizeError):
    """Raised when unlinking parent/child groups fails."""


class SetGroupPhotoError(NeonizeError):
    """Raised when setting a group photo fails."""


class SetGroupAnnounceError(NeonizeError):
    """Raised when toggling group announce mode fails."""


class SetGroupLockedError(NeonizeError):
    """Raised when toggling group lock fails."""


class SetGroupTopicError(NeonizeError):
    """Raised when setting the group topic/description fails."""


class UpdateGroupParticipantsError(NeonizeError):
    """Raised when updating group participants (promote/demote/remove) fails."""


# ---------------------------------------------------------------------------
# Newsletter / Channel
# ---------------------------------------------------------------------------


class CreateNewsletterError(NeonizeError):
    """Raised when creating a newsletter/channel fails."""


class FollowNewsletterError(NeonizeError):
    """Raised when following a newsletter fails."""


class UnfollowNewsletterError(NeonizeError):
    """Raised when unfollowing a newsletter fails."""


class GetNewsletterInfoError(NeonizeError):
    """Raised when retrieving newsletter information fails."""


class GetNewsletterInfoWithInviteError(NeonizeError):
    """Raised when resolving newsletter info from an invite link fails."""


class GetNewsletterMessagesError(NeonizeError):
    """Raised when fetching newsletter messages fails."""


class GetNewsletterMessageUpdateError(NeonizeError):
    """Raised when fetching newsletter message updates fails."""


class GetSubscribedNewslettersError(NeonizeError):
    """Raised when listing subscribed newsletters fails."""


class NewsletterMarkViewedError(NeonizeError):
    """Raised when marking a newsletter message as viewed fails."""


class NewsletterSendReactionError(NeonizeError):
    """Raised when sending a reaction to a newsletter message fails."""


class NewsletterSubscribeLiveUpdatesError(NeonizeError):
    """Raised when subscribing to newsletter live updates fails."""


class NewsletterToggleMuteError(NeonizeError):
    """Raised when toggling newsletter mute state fails."""


# ---------------------------------------------------------------------------
# Contact & Profile
# ---------------------------------------------------------------------------


class ContactStoreError(NeonizeError):
    """Raised when a contact store operation fails."""


class GetContactQrLinkError(NeonizeError):
    """Raised when retrieving a contact QR link fails."""


class GetProfilePictureError(NeonizeError):
    """Raised when retrieving a profile picture fails."""


class GetUserInfoError(NeonizeError):
    """Raised when retrieving user information fails."""


class GetUserDevicesError(NeonizeError):
    """Raised when listing a user's devices fails."""


class GetJIDFromStoreError(NeonizeError):
    """Raised when resolving a JID from the local store fails."""


class IsOnWhatsAppError(NeonizeError):
    """Raised when checking WhatsApp registration status fails."""


class PairPhoneError(NeonizeError):
    """Raised when pairing via phone number fails."""


class ResolveContactQRLinkError(NeonizeError):
    """Raised when resolving a contact QR link fails."""


class ResolveBusinessMessageLinkError(NeonizeError):
    """Raised when resolving a business message link fails."""


# ---------------------------------------------------------------------------
# Privacy & Status
# ---------------------------------------------------------------------------


class GetBlocklistError(NeonizeError):
    """Raised when retrieving the blocklist fails."""


class UpdateBlocklistError(NeonizeError):
    """Raised when updating the blocklist fails."""


class GetStatusPrivacyError(NeonizeError):
    """Raised when retrieving status privacy settings fails."""


class SetPrivacySettingError(NeonizeError):
    """Raised when changing a privacy setting fails."""


# ---------------------------------------------------------------------------
# Presence & Calls
# ---------------------------------------------------------------------------


class SendPresenceError(NeonizeError):
    """Raised when sending a presence update (typing/composing) fails."""


class SubscribePresenceError(NeonizeError):
    """Raised when subscribing to a user's presence fails."""


# ---------------------------------------------------------------------------
# Chat Settings
# ---------------------------------------------------------------------------


class GetChatSettingsError(NeonizeError):
    """Raised when retrieving local chat settings fails."""


class PutMutedUntilError(NeonizeError):
    """Raised when muting a chat until a specific time fails."""


class PutPinnedError(NeonizeError):
    """Raised when pinning/unpinning a chat fails."""


class PutArchivedError(NeonizeError):
    """Raised when archiving/unarchiving a chat fails."""


# ---------------------------------------------------------------------------
# State & Misc
# ---------------------------------------------------------------------------


class LogoutError(NeonizeError):
    """Raised when logging out fails."""


class MarkReadError(NeonizeError):
    """Raised when marking a message as read fails."""


class SendAppStateError(NeonizeError):
    """Raised when sending app state sync fails."""


class SetDefaultDisappearingTimerError(NeonizeError):
    """Raised when setting the default disappearing message timer fails."""


class SetDisappearingTimerError(NeonizeError):
    """Raised when setting a per-chat disappearing message timer fails."""


class SetPassiveError(NeonizeError):
    """Raised when toggling passive mode fails."""


class GetBusinessProfileError(NeonizeError):
    pass


class SetStatusMessageError(NeonizeError):
    """Raised when setting the status/about message fails."""


class SetProxyAddressError(NeonizeError):
    """Raised when configuring the proxy address fails."""


class UnsupportedEvent(NeonizeError):
    """Raised when an unrecognized event code is received from the Go core."""


class RejectCallError(NeonizeError):
    """Raised when rejecting an incoming call fails."""


class LeaveGroupError(NeonizeError):
    """Raised when leaving a group fails."""


class SetGroupNameError(NeonizeError):
    """Raised when renaming a group fails."""


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------


class ConvertStickerError(NeonizeError):
    """Raised when converting an image/video to sticker format fails."""


class FFProbeError(NeonizeError):
    """Raised when ffprobe fails to analyse a media file."""
