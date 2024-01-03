package utils

import (
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/types"
)

var MediaType = []whatsmeow.MediaType{
	whatsmeow.MediaImage,
	whatsmeow.MediaVideo,
	whatsmeow.MediaAudio,
	whatsmeow.MediaDocument,
	whatsmeow.MediaHistory,
	whatsmeow.MediaAppState,
	whatsmeow.MediaLinkThumbnail,
}

var ChatPresence = []types.ChatPresence{
	types.ChatPresenceComposing,
	types.ChatPresencePaused,
}

var ChatPresenceMedia = []types.ChatPresenceMedia{
	types.ChatPresenceMediaText,
	types.ChatPresenceMediaAudio,
}
