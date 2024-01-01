package utils

import (
	"C"

	"github.com/krypton-byte/neonize/neonize"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/types"
	"google.golang.org/protobuf/proto"
)

func EncodeUploadResponse(response whatsmeow.UploadResponse) neonize.UploadResponse {
	return neonize.UploadResponse{
		Url:           &response.URL,
		DirectPath:    &response.DirectPath,
		Handle:        &response.Handle,
		MediaKey:      response.MediaKey,
		FileEncSHA256: response.FileEncSHA256,
		FileSHA256:    response.FileSHA256,
		FileLength:    proto.Uint32(uint32(response.FileLength)),
	}
}
func EncodeJidProto(data types.JID) *neonize.JID {
	return &neonize.JID{
		User:       &data.User,
		RawAgent:   proto.Uint32(uint32(data.RawAgent)),
		Device:     proto.Uint32(uint32(data.Device)),
		Integrator: proto.Uint32(uint32(data.Integrator)),
		Server:     &data.Server,
	}
}
