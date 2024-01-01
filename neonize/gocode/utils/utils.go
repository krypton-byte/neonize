package utils

import "go.mau.fi/whatsmeow"

var MediaType = map[int]whatsmeow.MediaType{
	1: whatsmeow.MediaImage,
	2: whatsmeow.MediaVideo,
	3: whatsmeow.MediaAudio,
	4: whatsmeow.MediaDocument,
	5: whatsmeow.MediaHistory,
	6: whatsmeow.MediaAppState,
	7: whatsmeow.MediaLinkThumbnail,
}
