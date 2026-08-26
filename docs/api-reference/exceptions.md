# Exceptions

All Neonize errors live in `neonize.exc` and derive from `Exception`. There
is one exception class per failing operation, so `except` clauses can be as
narrow or broad as you like.

## Hierarchy

```text
Exception
└── NeonizeError            (base for library-level errors)
    └── UnsupportedEvent
Exception
├── UploadError / DownloadError
├── SendMessageError
├── PairPhoneError
├── CreateGroupError
├── ... (one class per operation, see table below)
└── ContactStoreError / FFProbeError / ConvertStickerError
```

`NeonizeError` is the semantic base class; most operation errors currently
derive directly from `Exception`, so catch concrete classes for precise
handling.

## Operation Errors

| Exception | Raised by |
| --- | --- |
| `PairPhoneError` | `PairPhone` |
| `SendMessageError` | `send_message`, media sends |
| `UploadError` / `DownloadError` | Media upload / download |
| `CreateGroupError` | `create_group` |
| `GetGroupInfoError` | `get_group_info*` |
| `SetGroupPhotoError` | `set_group_photo` |
| `GetGroupInviteLinkError` | `get_group_invite_link` |
| `InviteLinkError` | Link parsing/resolution |
| `JoinGroupWithInviteError` | `join_group_with_invite` |
| `LinkGroupError` / `UnlinkGroupError` | Community linking |
| `GetLinkedGroupParticipantsError` | `get_linked_group_participants` |
| `GetGroupRequestParticipantsError` | `get_group_request_participants` |
| `UpdateGroupParticipantsError` | `update_group_participants` |
| `IsOnWhatsAppError` | `is_on_whatsapp` |
| `GetUserInfoError` | `get_user_info` |
| `GetUserDevicesError` | `get_user_devices` |
| `GetProfilePictureError` | `get_profile_picture` |
| `GetStatusPrivacyError` | `get_status_privacy` |
| `MarkReadError` | `mark_read` |
| `BuildPollVoteError` / `BuildPollVoteCreationError` / `DecryptPollVoteError` | Poll flows |
| `CreateNewsletterError` | `create_newsletter` |
| `FollowNewsletterError` / `UnfollowNewsletterError` | Channel follow state |
| `GetNewsletterInfoError` / `GetNewsletterInfoWithInviteError` | Channel lookup |
| `GetNewsletterMessagesError` / `GetNewsletterMessageUpdateError` | Channel history |
| `NewsletterSendReactionError` / `NewsletterMarkViewedError` / `NewsletterSubscribeLiveUpdatesError` / `NewsletterToggleMuteError` | Channel actions |
| `GetSubscribedNewslettersError` | `get_subscribed_newletters` |
| `SendPresenceError` | `send_presence` |
| `SubscribePresenceError` | `subscribe_presence` |
| `SetPrivacySettingError` | `set_privacy_setting` |
| `SetDefaultDisappearingTimerError` / `SetDisappearingTimerError` | Disappearing timers |
| `SetGroupAnnounceError` / `SetGroupLockedError` / `SetGroupTopicError` | Group settings |
| `GetBlocklistError` / `UpdateBlocklistError` | Blocking |
| `ResolveContactQRLinkError` / `ResolveBusinessMessageLinkError` / `GetContactQrLinkError` | QR/business links |
| `SendAppStateError` / `SetPassiveError` / `SetProxyAddressError` | Protocol/config |
| `LogoutError` | `logout` |
| `GetJoinedGroupsError` / `GetSubGroupsError` | Group discovery |
| `GetJIDFromStoreError` | Store lookups |

## Client-Side Errors

| Exception | Meaning |
| --- | --- |
| `UnsupportedEvent` | Dispatch of an event type with no registered handler path |
| `ContactStoreError` | Local contact database failure |
| `FFProbeError` | FFmpeg probe failed (media inspection) |
| `ConvertStickerError` | Sticker conversion failed — check FFmpeg installation |
| `PutMutedUntilError` / `PutPinnedError` / `PutArchivedError` / `GetChatSettingsError` | Chat settings store |

## Handling Pattern

```python
from neonize.exc import IsOnWhatsAppError, GetUserInfoError

try:
    rows = client.is_on_whatsapp([target])
except IsOnWhatsAppError:
    # protocol failure — retry later or log and continue
    ...
```
