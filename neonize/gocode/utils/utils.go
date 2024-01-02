package utils

import (
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/types"
)

var MediaType = map[int]whatsmeow.MediaType{
	1: whatsmeow.MediaImage,
	2: whatsmeow.MediaVideo,
	3: whatsmeow.MediaAudio,
	4: whatsmeow.MediaDocument,
	5: whatsmeow.MediaHistory,
	6: whatsmeow.MediaAppState,
	7: whatsmeow.MediaLinkThumbnail,
}

var ChatPresence = map[int]types.ChatPresence{
	0: types.ChatPresenceComposing,
	1: types.ChatPresencePaused,
}

var ChatPresenceMedia = map[int]types.ChatPresenceMedia{
	0: types.ChatPresenceMediaText,
	1: types.ChatPresenceMediaAudio,
}
