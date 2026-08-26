# Exceptions

All Neonize errors live in `neonize.exc` and inherit from
`NeonizeError`. There is one exception class per failing operation, so
`except` clauses can be as narrow or broad as you like.

```python
from neonize.exc import NeonizeError

try:
    client.send_message("6281234567890", "hello")
except NeonizeError as exc:
    print(f"Library error: {exc}")
```

## Hierarchy

```text
NeonizeError
├── Transport:      UploadError, DownloadError
├── Messaging:      SendMessageError, BuildPollVoteError, ...
├── Group:          CreateGroupError, LeaveGroupError, SetGroupNameError, ...
├── Newsletter:     CreateNewsletterError, FollowNewsletterError, ...
├── Contact:        ContactStoreError, GetUserInfoError, PairPhoneError, ...
├── Privacy:        GetBlocklistError, SetPrivacySettingError, ...
├── Presence:       SendPresenceError, SubscribePresenceError, ...
├── Chat Settings:  PutMutedUntilError, PutPinnedError, ...
├── State:          LogoutError, UnsupportedEvent, ...
└── Media:          ConvertStickerError, FFProbeError
```

Every exception listed in the table below is a subclass of
`NeonizeError`, so a single `except NeonizeError` catches all of them.

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
| `SendPresenceError` | `send_presence`, `send_chat_presence` |
| `SubscribePresenceError` | `subscribe_presence` |
| `RejectCallError` | `reject_call` |
| `LeaveGroupError` | `leave_group` |
| `SetGroupNameError` | `set_group_name` |
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
