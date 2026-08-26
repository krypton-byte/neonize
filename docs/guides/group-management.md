# Group Management

Group JIDs use the `g.us` server. Every method below takes or returns `JID`
objects — see [JID and Addressing](../core-concepts/jid-and-addressing.md).

## Creating a Group

```python
from neonize.utils import build_jid

group = client.create_group(
    "Project Team",
    [build_jid("628123456789"), build_jid("628987654321")],
)
info: GroupInfo = client.get_group_info(group.JID)
```

## Discovering Groups

```python
groups = client.get_joined_groups()        # list of linked-group metadata
for g in groups:
    print(g.GroupName, g.JID)
```

Community sub-groups are reachable through `get_sub_groups(parent_jid)` and
`get_linked_group_participants(group_jid)`.

## Metadata and Invite Links

```python
info = client.get_group_info(group_jid)          # name, topic, participants, settings
info2 = client.get_group_info_from_link("https://chat.whatsapp.com/AbCdEf")
invite = client.get_group_invite_link(group_jid) # generate a shareable link
```

## Joining

```python
client.join_group_with_link("https://chat.whatsapp.com/AbCdEf")
# or resolve first:
meta = client.get_group_info_from_invite("AbCdEf")
client.join_group_with_invite(meta)
```

## Participants

All operations take a list of JIDs plus an action:

```python
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    ParticipantChangeType,   # ADD | REMOVE | PROMOTE | DEMOTE
)

client.update_group_participants(
    group_jid, [build_jid("628123456789")], ParticipantChangeType.ADD
)
```

Pending join requests can be inspected with
`get_group_request_participants`.

## Settings

| Method | Purpose | Raises |
| --- | --- | --- |
| `set_group_name(jid, name)` | Rename the group | `SetGroupNameError` |
| `set_group_topic(jid, topic)` | Set description/topic | `SetGroupTopicError` |
| `set_group_photo(jid, path_or_bytes)` | Change the picture | `SetGroupPhotoError` |
| `set_group_announce(jid, locked)` | Only admins may send messages | `SetGroupAnnounceError` |
| `set_group_locked(jid, locked)` | Only admins may edit group info | `SetGroupLockedError` |

```python
client.set_group_name(group_jid, "New Name")
client.set_group_announce(group_jid, True)      # admin-only chat
```

## Leaving and Linking

```python
client.leave_group(group_jid)          # raises LeaveGroupError on failure
```

Communities (linked groups) connect child groups to a parent:

```python
client.link_group(child_jid, parent_jid)
client.unlink_group(child_jid, parent_jid)
```

`create_group` also accepts `linked_parent=` / `group_parent=` to create
directly inside a community.

## JoinedGroup Event

When the bot is added to a group you receive `JoinedGroupEv`, which since
v0.4.3 carries who performed the add:

```python
from neonize.events import JoinedGroupEv

@client.event(JoinedGroupEv)
def on_joined(client: NewClient, ev: JoinedGroupEv) -> None:
    if ev.Sender is not None:
        print(f"Added by {ev.Sender.User}")
    client.send_message(ev.JID, "Thanks for adding me! Type /help.")
```

Ongoing changes to groups you are in arrive as `GroupInfoEv`.
