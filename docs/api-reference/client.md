# Sync Client (`NewClient`)

The synchronous client. Construct it with the path of the SQLite session
database, register event handlers, and connect.

```python
from neonize.client import NewClient

client = NewClient("session.db")
```

## Constructor

::: neonize.client.NewClient
    options:
      members:
        - __init__
        - connect
        - connect_with_proxy
        - disconnect
        - stop
        - logout
        - get_me
        - set_passive
        - set_force_activate_delivery_receipts

## Sending

::: neonize.client.NewClient
    options:
      members:
        - send_message
        - reply_message
        - edit_message
        - revoke_message
        - build_revoke
        - build_reaction
        - send_image
        - send_video
        - send_audio
        - send_document
        - send_sticker
        - send_stickerpack
        - send_album
        - send_contact
        - send_interactive_message
        - send_fb_message
        - pin_message
        - mark_read
        - upload

## Message Builders

::: neonize.client.NewClient
    options:
      members:
        - build_image_message
        - build_video_message
        - build_audio_message
        - build_document_message
        - build_sticker_message
        - build_stickerpack_message
        - build_album_content
        - build_reply_message
        - build_poll_vote_creation
        - build_poll_vote

## Media Download

::: neonize.client.NewClient
    options:
      members:
        - download_any
        - download_media_with_path

## Groups

::: neonize.client.NewClient
    options:
      members:
        - create_group
        - get_joined_groups
        - get_group_info
        - get_group_info_from_link
        - get_group_info_from_invite
        - get_group_invite_link
        - join_group_with_link
        - join_group_with_invite
        - update_group_participants
        - get_group_request_participants
        - get_linked_group_participants
        - get_sub_groups
        - set_group_name
        - set_group_topic
        - set_group_photo
        - set_group_announce
        - set_group_locked
        - leave_group
        - link_group
        - unlink_group

## Contacts and Presence

::: neonize.client.NewClient
    options:
      members:
        - is_on_whatsapp
        - get_user_info
        - get_user_devices
        - get_profile_picture
        - get_contact_qr_link
        - resolve_contact_qr_link
        - resolve_business_message_link
        - subscribe_presence
        - send_presence
        - send_chat_presence
        - get_privacy_settings
        - set_privacy_setting
        - get_blocklist
        - update_blocklist
        - get_lid_from_pn
        - get_pn_from_lid
        - reject_call

## Profile

::: neonize.client.NewClient
    options:
      members:
        - set_profile_name
        - set_profile_photo
        - set_status_message
        - set_default_disappearing_timer
        - set_disappearing_timer
        - get_status_privacy

## Newsletters (Channels)

::: neonize.client.NewClient
    options:
      members:
        - create_newsletter
        - get_newsletter_info
        - get_newsletter_info_with_invite
        - follow_newsletter
        - unfollow_newsletter
        - get_newsletter_messages
        - get_newsletter_message_update
        - newsletter_send_reaction
        - newsletter_mark_viewed
        - newsletter_subscribe_live_updates
        - newsletter_toggle_mute
        - upload_newsletter
        - get_subscribed_newletters

## Utilities

::: neonize.client.NewClient
    options:
      members:
        - generate_message_id
        - decrypt_poll_vote
        - get_message_for_retry
        - send_app_state
        - PairPhone
        - set_proxy_address
