# Events

Typed event classes dispatched by the event system. The async module
`neonize.aioze.events` re-exports the same catalog.

## Dispatcher

::: neonize.events.Event
    options:
      members:
        - __call__

::: neonize.events.event
    options:
      members: false

## Connection Lifecycle

::: neonize.events.QREv
    options:
      members: false

::: neonize.events.PairStatusEv
    options:
      members: false

::: neonize.events.ConnectedEv
    options:
      members: false

::: neonize.events.DisconnectedEv
    options:
      members: false

::: neonize.events.StreamReplacedEv
    options:
      members: false

::: neonize.events.KeepAliveTimeoutEv
    options:
      members: false

::: neonize.events.KeepAliveRestoredEv
    options:
      members: false

::: neonize.events.ClientOutdatedEv
    options:
      members: false

::: neonize.events.LoggedOutEv
    options:
      members: false

## Messaging

::: neonize.events.MessageEv
    options:
      members: false

::: neonize.events.UndecryptableMessageEv
    options:
      members: false

::: neonize.events.ReceiptEv
    options:
      members: false

::: neonize.events.ChatPresenceEv
    options:
      members: false

::: neonize.events.IdentityChangeEv
    options:
      members: false

## Groups

::: neonize.events.GroupInfoEv
    options:
      members: false

::: neonize.events.JoinedGroupEv
    options:
      members: false

::: neonize.events.PictureEv
    options:
      members: false

## Newsletters

::: neonize.events.NewsletterJoinEv
    options:
      members: false

::: neonize.events.NewsletterLeaveEv
    options:
      members: false

::: neonize.events.NewsletterMuteChangeEv
    options:
      members: false

::: neonize.events.NewsLetterMessageMetaEv
    options:
      members: false

## Calls

::: neonize.events.CallOfferEv
    options:
      members: false

::: neonize.events.CallAcceptEv
    options:
      members: false

::: neonize.events.CallPreAcceptEv
    options:
      members: false

::: neonize.events.CallOfferNoticeEv
    options:
      members: false

::: neonize.events.CallTerminateEv
    options:
      members: false

::: neonize.events.CallTransportEv
    options:
      members: false

## Privacy, Sync and Errors

::: neonize.events.PrivacySettingsEv
    options:
      members: false

::: neonize.events.BlocklistEv
    options:
      members: false

::: neonize.events.BlocklistChangeEv
    options:
      members: false

::: neonize.events.HistorySyncEv
    options:
      members: false

::: neonize.events.OfflineSyncPreviewEv
    options:
      members: false

::: neonize.events.OfflineSyncCompletedEv
    options:
      members: false

::: neonize.events.ConnectFailureEv
    options:
      members: false

::: neonize.events.StreamErrorEv
    options:
      members: false

::: neonize.events.TemporaryBanEv
    options:
      members: false

For when each event fires, see the annotated table in
[Event Model](../core-concepts/event-model.md).
